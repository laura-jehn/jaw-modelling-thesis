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
import maspack.matrix.Vector3d;
import maspack.matrix.VectorNd;
import maspack.spatialmotion.Wrench;

public class CondyleTrajectoryDemo extends JawLarynxDemo {
   
   boolean inc = true;
   
   public void build (String[] args) throws IOException {
      super.build (args);
   }
   
   public void attach(DriverInterface driver) {
      workingDirname = "data/incisorForce";
      probesFilename = "incisorDispProbes.art";
      super.attach(driver);
      
      addBreakPoint(2.0);
   }
   
   public StepAdjustment advance (double t0, double t1, int flags) {
      
      /*double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
      double closers_excitation = (double) myJawModel.getProperty ("exciters/bi_close:excitation").get ();
      
      if(openers_excitation >= 0.03) {
         inc = false;
      }
      if(inc) {
         myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
      } else if(closers_excitation < 1.0){
         myJawModel.getProperty ("exciters/bi_open:excitation").set (0);
         myJawModel.getProperty ("exciters/bi_close:excitation").set (closers_excitation+0.005);
      }*/
      
      double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
      if(openers_excitation >= 0.4) {
         inc = false;
      }
      if(inc) {
         myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
      } else if(openers_excitation > 0.005){
         myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation-0.005);
      }
      
      StepAdjustment sa = super.advance (t0, t1, flags);
      return sa;
   }
}
