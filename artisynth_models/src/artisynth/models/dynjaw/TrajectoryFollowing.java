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

public class TrajectoryFollowing extends JawLarynxDemo {
   
   PointForce myPointForce;
   NumericControlProbe trajectory;
   
   // Kp parameter of controller
   double Kp = 15;
   // Kv parameter of controller
   double Kv = 0.005;
   // sampling time
   double ts = 0.001;
   
   Vector3d err_prev = new Vector3d();
  
   
   /** attributes for jython **/
   double xError = 0;
   Vector3d xIs = new Vector3d();
   Vector3d xShould = new Vector3d();
   
   // frame marker for current target position of trajectory, initialized to IP at teeth occlusion
   FrameMarker targetIP = new FrameMarker(0.0, -47.9584, 41.7642);
   
   // this function contains the control routine
   public class TrajectoryControlFunction implements DataFunction{
      
      // vec contains the current target IP (at timestep t)
      public void eval(VectorNd vec, double t, double trel) {     
         // reset error
    	 if(t==0) {
            xError=0;
         }
    	 
    	 // find position of lower incisors
         Vector3d li = myJawModel.frameMarkers().findComponent ("lowerincisor").getPosition ();
         // x_is is displacement of lower incisors (subtracting their initial position (at teeth occlusion))
         xIs = new Vector3d().sub (li, new Vector3d(0.0, -47.9584, 41.7642));
         
         // nächster soll-Wert laden
         xShould = new Vector3d(vec.get (0), vec.get (1), vec.get (2));
         
         // for visualising the given trajectory
         targetIP.setPosition (xIs.x, xShould.y-47.9584, xShould.z+41.7642);
         
         Vector3d err = new Vector3d().sub (xShould, xIs);
         
         // f = Kp * err + Kv * (err - err_prev)/ts
         Vector3d f = new Vector3d().add (new Vector3d().scale (Kp, err), (new Vector3d().sub (err, err_prev)).scale (1/ts).scale(Kv));
         //System.out.println("f: " + f.toString ());
         
         xError += Math.pow (err.norm (), 2);
         
         myPointForce.setForce (f.scale (1000)); // scale Newton to internal force units
         
         //System.out.println("Newton: " + myPointForce.getMagnitude()/1000);
         
         myPointForce.setAxisLength (myPointForce.getMagnitude ()/1000);
         
         err_prev = err.clone ();
      }
   }
   
   /** public access methods for jython **/
   public double getXError() {
      return xError;
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
      RenderProps.setLineColor(targetIP, Color.RED);
      RenderProps.setPointColor(targetIP, Color.RED);
      Point3d loc = new Point3d();
      targetIP.getLocation(loc);
      targetIP.setLocation(loc);
      enableTracing (targetIP);
   }

   public void build (String[] args) throws IOException {
      super.build (args);

      FrameMarker mkr =
         (FrameMarker)myJawModel.findComponent ("frameMarkers/lowerincisor");
      myPointForce = new PointForce (mkr);

      // add external force effector
      myJawModel.addForceEffector (myPointForce);

      RenderProps.setLineStyle (myPointForce, Renderer.LineStyle.CYLINDER);
      RenderProps.setLineRadius (myPointForce, 0.5);
      RenderProps.setLineColor (myPointForce, Color.GREEN);
      myPointForce.setAxisLength (myPointForce.getMagnitude ());
      
      workingDirname="data/controlchew";
      setWorkingDir();
      // chewingTrajectory.txt contains the trajectory to be followed
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
