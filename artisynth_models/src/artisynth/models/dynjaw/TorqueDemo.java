package artisynth.models.dynjaw;

import java.io.IOException;
import artisynth.core.mechmodels.Frame;
import artisynth.core.mechmodels.FrameMarker;
import artisynth.core.mechmodels.RigidBody;
import artisynth.core.modelbase.StepAdjustment;
import artisynth.core.probes.NumericMonitorProbe;
import artisynth.core.workspace.DriverInterface;
import artisynth.core.probes.DataFunction;
import maspack.matrix.Point3d;
import maspack.matrix.RigidTransform3d;
import maspack.matrix.RotationMatrix3d;
import maspack.matrix.Vector3d;
import maspack.matrix.VectorNd;
import maspack.render.RenderProps;
import maspack.spatialmotion.Wrench;

/* This class determines rotation and translation of the mandible
 * and calculates torques for producing sample forces at the lower incisors.
 *  */

public class TorqueDemo extends JawDemo {
   
   // type of performed movement
   // 0 for opening, 1 for chewing
   int movementType = 0;
   
   FrameMarker lowerIncisor;
   // incisor frame
   Frame incFrame = new Frame();
   // instantaneous frame
   Frame mi = new Frame();
   // initial position of center of condylar axis
   RigidTransform3d XFrameToWorld = new RigidTransform3d(0, 31.4501, 79.637); 
   
   Vector3d liPos_mi = new Vector3d(0, -79.4085, -37.8728);
   
   private class MIPose implements DataFunction{
      
      // determines position and orientation of the instantaneous frame each time step
      public void eval(VectorNd vec, double t, double trel) {
               
         // roll pitch yaw values of incisor frame
         RigidTransform3d m = incFrame.getPose ();
         double[] rpy = new double[3];
         m.R.getRpy (rpy);
         
         // calculate midpoint of condylar axis
         Point3d rtmj = ((FrameMarker)myJawModel.findComponent ("frameMarkers/rtmj")).getPosition ();
         Point3d ltmj = ((FrameMarker)myJawModel.findComponent ("frameMarkers/ltmj")).getPosition ();
         Point3d condylarAxisCenter = new Point3d();
         condylarAxisCenter.add (rtmj, ltmj).scale (0.5);
         
         // set mi position at condylarAxisCenter and set mi rotation equal to inc frame rotation
         RigidTransform3d r = new RigidTransform3d();
         r.setRpy (rpy[0], rpy[1], rpy[2]);
         r.setTranslation (condylarAxisCenter);
         mi.setPose (r);
         
         //System.out.println("Rotation angles: " + Math.toDegrees (rpy[0]) + " " + Math.toDegrees (rpy[1]) + " " + Math.toDegrees (rpy[2]));
         
         // get incisor position relative to the mandible frame
         Point3d liPos = lowerIncisor.getPosition();
         Vector3d liPos_mo = new Vector3d().sub (liPos, XFrameToWorld.p);
         
         // output incisor position
         vec.setSubVector (0, liPos_mo);
         
         // output displacement of instantaneous frame
         vec.set (3, condylarAxisCenter.x);
         vec.set (4, condylarAxisCenter.y - 31.4501);
         vec.set (5, condylarAxisCenter.z - 79.637);
         
         // output rotation of instantaneous frame
         // rpy order reversed from z, y, x angles to x, y, z angles
         vec.set (6, Math.toDegrees (rpy[2]));
         vec.set (7, Math.toDegrees (rpy[1]));
         vec.set (8, Math.toDegrees (rpy[0]));
         
         // output torques for producing forces
         // (unit vectors of the world coordinate axes of the coordinate system of the kinematic model)
         Wrench wr = new Wrench();
         mi.computeAppliedWrench (wr, new Vector3d(0, -1, 0), liPos_mi);
         vec.setSubVector (9, wr.m.clone ());
         mi.computeAppliedWrench (wr, new Vector3d(1, 0, 0), liPos_mi);
         vec.setSubVector (12, wr.m.clone ());
         mi.computeAppliedWrench (wr, new Vector3d(0, 0, 1), liPos_mi);
         vec.setSubVector (15, wr.m.clone ());
         
      }
   }

   // add probe for MIPose to the model
   public void addMIPoseProbe() {
      NumericMonitorProbe p = new NumericMonitorProbe (/*vsize=*/18, "MIPose.txt", 0, 10, 0.01);
      p.setDataFunction (new MIPose());
      p.setName("MIPose");
      addOutputProbe(p); 
   }
   
   public void build (String[] args) throws IOException {
      super.build (args);
      
      lowerIncisor = (FrameMarker)myJawModel.findComponent ("frameMarkers/lowerincisor");
      
      incFrame.setPosition(lowerIncisor.getPosition ());
      myJawModel.add(incFrame);
      mi.setAxisLength (10);
      myJawModel.add(mi);
      
      RigidBody jaw = (RigidBody) myJawModel.rigidBodies ().get ("jaw");
      myJawModel.attachFrame(incFrame, jaw);
      
      RigidBody maxilla = (RigidBody) myJawModel.rigidBodies ().get ("maxilla");
      RenderProps.setVisible (maxilla, true);
   }
   
   public void attach(DriverInterface driver) {
      if(movementType == 1) {
         workingDirname = "data/controlchew";
         probesFilename = "rightchew.art";
      }
      
      super.attach(driver);
      addMIPoseProbe();
   }
   
   public StepAdjustment advance (double t0, double t1, int flags) {
      
      if(movementType == 0) {
         double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
         if(openers_excitation < 1.0) {
            myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
         }
      }
      
      StepAdjustment sa = super.advance (t0, t1, flags);
      return sa;
   }
}
