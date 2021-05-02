package artisynth.models.dynjaw;

import java.awt.Color;
import java.io.IOException;
import java.util.ArrayList;

import artisynth.core.femmodels.FemGeometryTransformer;
import artisynth.core.femmodels.FemNode3d;
import artisynth.core.mechmodels.FrameMarker;
import artisynth.core.mechmodels.PointForce;
import artisynth.core.modelbase.StepAdjustment;
import artisynth.core.modelbase.TransformGeometryContext;
import artisynth.core.probes.NumericControlProbe;
import artisynth.core.probes.DataFunction;
import artisynth.core.workspace.DriverInterface;
import artisynth.core.workspace.FemModelDeformer;
import maspack.geometry.GeometryTransformer;
import maspack.matrix.AxisAlignedRotation;
import maspack.matrix.Point3d;
import maspack.matrix.Vector3d;
import maspack.matrix.VectorNd;
import maspack.render.RenderProps;
import maspack.render.Renderer;
import maspack.render.GL.GLViewer;

public class ControlJawDemo extends JawLarynxDemo {
   
   PointForce myPointForce;
   NumericControlProbe trajectory;
   
   double Kp = 15;
   double Kv = 0.005;
   double ts = 0.001; // sampling time
   
   Vector3d err_prev = new Vector3d();
  
   
   /** attributes for jython **/
   double xError = 0;
   Vector3d xIs = new Vector3d();
   Vector3d xShould = new Vector3d();
   FrameMarker givenTrajectory = new FrameMarker(0.0, -47.9584, 41.7642);
   
   
   public class TrajectoryControlFunction implements DataFunction{
      
      public void eval(VectorNd vec, double t, double trel) {
                
         // reset error
    	 if(t==0) {
            xError=0;
         }
    	 // find position of lower incisors
         Vector3d li = myJawModel.frameMarkers().findComponent ("lowerincisor").getPosition ();
         // get displacement of lower incisors by subtracting the initial position
         Vector3d x_is = new Vector3d().sub (li, new Vector3d(0.0, -47.9584, 41.7642));
         
         // nächster soll-Wert laden
         Vector3d x_should = new Vector3d(vec.get (0), vec.get (1), vec.get (2));
         
         setXIs(x_is);
         xShould = x_should;
         
         // for visualising the given trajectory
         givenTrajectory.setPosition (x_should.x, x_should.y-47.9584, x_should.z+41.7642);
         
         Vector3d err = new Vector3d().sub (x_should, x_is);
         
         // f = Kp * err + Kv * (err - err_prev)/ta
         Vector3d f = new Vector3d().add (new Vector3d().scale (Kp, err), (new Vector3d().sub (err, err_prev)).scale (1/ts).scale(Kv));
         //System.out.println("f: " + f.toString ());
         
         xError += Math.pow (err.norm (), 2);
         
         myPointForce.setForce (f.scale (1000));
         
         //System.out.println("Newton: " + myPointForce.getMagnitude()/1000);
         System.out.println(myPointForce.getForce().toString ());
         myPointForce.setAxisLength (myPointForce.getMagnitude ()/1000);
         
         err_prev = err.clone ();
         
         //System.out.println("RMSE: " + Math.sqrt (xError));
      }
   }
   
   /** public access methods for jython **/
   public double getXError() {
      return xError;
   }
   
   public void setXIs(Vector3d xIs) {
      this.xIs = xIs;
   }
   
   public Vector3d getXIs() {
      return xIs;
   }
   
   public Vector3d getXShould() {
      return xShould;
   }
   
   public void resetXError() {
      xError = 0;
      err_prev.setZero ();
   }
   
   public Vector3d getForce() {
      return myPointForce.getForce ();
   }
   
   public void setKp(double Kp) {
      this.Kp = Kp;
   }
   
   public void setKv(double Kv) {
      this.Kv = Kv;
   }
   
   
   public void setVisible() {
      RenderProps.setLineColor(givenTrajectory, Color.RED);
      RenderProps.setPointColor(givenTrajectory, Color.RED);
      Point3d loc = new Point3d();
      givenTrajectory.getLocation(loc);
      givenTrajectory.setLocation(loc);
      enableTracing (givenTrajectory);
   }

   public void build (String[] args) throws IOException {
      super.build (args);

      FrameMarker mkr =
         (FrameMarker)myJawModel.findComponent ("frameMarkers/lowerincisor");
      myPointForce = new PointForce (mkr);

      myJawModel.addForceEffector (myPointForce);

      RenderProps.setLineStyle (myPointForce, Renderer.LineStyle.CYLINDER);
      RenderProps.setLineRadius (myPointForce, 0.5);
      RenderProps.setLineColor (myPointForce, Color.GREEN);
      myPointForce.setAxisLength (myPointForce.getMagnitude ());
      
      workingDirname="data/controlchew";
      setWorkingDir();
      trajectory = new NumericControlProbe("chewingTrajectory.txt");
      trajectory.setVsize (3);
      trajectory.load ();
      trajectory.setDataFunction (new TrajectoryControlFunction());
      trajectory.setName ("trajectory");
   }
   
   public void attach(DriverInterface driver) {
      workingDirname="data/controlchew";
      probesFilename = "rightchew.art";
      super.attach(driver);
      
      addInputProbe(trajectory);
      setVisible();
      
      setIncisorVisible();
      addBreakPoint(0.55);
   }
}
