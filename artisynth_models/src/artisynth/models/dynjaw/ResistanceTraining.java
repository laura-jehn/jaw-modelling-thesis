package artisynth.models.dynjaw;

import java.awt.Color;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import artisynth.core.gui.ControlPanel;
import artisynth.core.mechmodels.FrameMarker;
import artisynth.core.mechmodels.PointForce;
import artisynth.core.mechmodels.RigidBody;
import artisynth.core.modelbase.ComponentUtils;
import artisynth.core.modelbase.StepAdjustment;
import artisynth.core.util.ArtisynthPath;
import artisynth.core.workspace.DriverInterface;
import artisynth.models.dynjaw.JawModel.CondylarSlopeType;
import artisynth.models.dynjaw.ResistanceDemo.MovementState;
import maspack.matrix.Point3d;
import maspack.matrix.Vector3d;
import maspack.render.RenderProps;
import maspack.render.Renderer;

public class ResistanceTraining extends JawLarynxDemo {
   
   PointForce force;
   FrameMarker li;
   ArrayList<Point3d> movementHistory = new ArrayList<Point3d>();
   
   // li at rest
   Point3d liInit = new Point3d(0, -47.9584, 41.7642);
   
   boolean inc = true;
   
   public enum TrainingType {
      OPENING("opening", 2, -1, 50), LEFT_LATEROTRUSION("llat", 0, 1, 10), RIGHT_LATEROTRUSION("rlat", 0, -1, 10);
      
      String trainingName;
      int axis;
      int sign;
      int incSize;
      
      private TrainingType (String trainingName, int axis, int sign, int incSize) {
         this.trainingName = trainingName;
         this.axis = axis;
         this.sign = sign;
         this.incSize = incSize;
      }
      
      public String getTrainingName() {
         return trainingName;
      }

      public int getAxis() {
         return axis;
      }

      public int getSign() {
         return sign;
      }
      
      public int getIncSize() {
         return this.incSize;
      }
   }

   TrainingType trainingType = TrainingType.OPENING;
   
   public TrainingType getTrainingType() {
      return trainingType;
   }
   
   public TrainingType setTrainingType(TrainingType trainingType) {
      return this.trainingType = trainingType;
   }
   
   public String getForce() {
      return force.getForce ().toString ();
   }
   
   enum MovementState {IN_MOVEMENT, AT_LIMIT, MOVEMENT_BACK, IDLE};
   MovementState movementState = MovementState.IDLE;
   
   public void reset() {
      inc = true;
      force.setForce (new Vector3d());
   }
   
   public void build (String[] args) throws IOException {
      super.build (args);
      
      li = (FrameMarker)myJawModel.findComponent ("frameMarkers/lowerincisor");
      force = new PointForce (li);
      myJawModel.addForceEffector (force);
      
      RenderProps.setLineStyle (force, Renderer.LineStyle.CYLINDER);
      RenderProps.setLineRadius (force, 0.5);
      RenderProps.setLineColor (force, Color.GREEN);
   }
   
   public StepAdjustment advance (double t0, double t1, int flags) {
      int incSize = trainingType.getIncSize ();
      
      Point3d li_pos = li.getPosition ();
      // displacement of lower incisors
      Point3d li_displ = (Point3d)new Point3d().sub (li_pos, liInit);
      double displ_dist = li_displ.norm ();
      
      System.out.println("displ_dist: " + displ_dist);
           
      // always keep 10 previous li positions
      int noPreviousPoints = movementHistory.size ();
      movementHistory.add (li_pos.clone ());
      if(noPreviousPoints > 10) {
         movementHistory.remove (0);
      }
      
      // determine direction in which jaw is moving
      Point3d dir = new Point3d();
      if(movementHistory.size () > 1) {
         dir.sub (movementHistory.get(0), movementHistory.get(noPreviousPoints-1));
      }
      
      double velocity = dir.norm();
      
      if(velocity < 0.005) {
         // jaw is not moving
         double mag = force.getMagnitude ();
         switch(movementState) {
            case IN_MOVEMENT:
               movementState = MovementState.AT_LIMIT;
               force.setMagnitude (mag-incSize > 0 ? mag-incSize : 0);
               System.out.println("set force to " + force.getForce().toString() + " N");
               break;
            case MOVEMENT_BACK:
               movementState = MovementState.IDLE;
               break;
            default: // movementState does not change
         }
      } else {
         // only update force when jaw is moving         
         int i = trainingType.getAxis ();
         int sign = trainingType.getSign ();
         
         if(-1 * sign * dir.get (i) / dir.norm () > 0.85 ){
            movementState = MovementState.IN_MOVEMENT;
            double mag = force.getMagnitude ();
            force.setMagnitude (mag+incSize);
            
            Point3d direction = new Point3d();
            direction.set (i, -1 * sign);
            force.setDirection(direction);
            
            System.out.println("set force to " + force.getMagnitude ()/1000 + " N");
            
         } else { 
           movementState = MovementState.MOVEMENT_BACK;
           double mag = force.getMagnitude ();
           force.setMagnitude (mag-incSize > 0 ? mag-incSize : 0);
         }   
         
      }
      
      force.setAxisLength (force.getMagnitude ()/100);
      
      double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
      double lip_excitation = (double) myJawModel.getProperty ("axialSprings/lip:excitation").get ();
      double rip_excitation = (double) myJawModel.getProperty ("axialSprings/rip:excitation").get ();
      
      switch(trainingType) {
         case OPENING:            
            if(openers_excitation >= 0.5){
               inc = false;
            }
            if(inc) {
               myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.0025);
            } else if(openers_excitation > 0.0){
               myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation-0.005);
            }
            break;
         case LEFT_LATEROTRUSION:
            myJawModel.getProperty ("exciters/bi_open:excitation").set (0.00);
            if(rip_excitation >= 1.0){
               inc = false;
            }
            if(inc) {
               myJawModel.getProperty ("axialSprings/rip:excitation").set (rip_excitation+0.0025);
            } else if(rip_excitation > 0.0) {
               myJawModel.getProperty ("axialSprings/rip:excitation").set (rip_excitation-0.005);
            }
            break;
         case RIGHT_LATEROTRUSION:
            myJawModel.getProperty ("exciters/bi_open:excitation").set (0.01);
            if(lip_excitation >= 1.0){
               inc = false;
            }
            if(inc) {
               myJawModel.getProperty ("axialSprings/lip:excitation").set (lip_excitation+0.0025);
            } else if(lip_excitation > 0.0) {
               myJawModel.getProperty ("axialSprings/lip:excitation").set (lip_excitation-0.005);
            }
            break;
          default: // no muscle activation
            
      }
      
      StepAdjustment sa = super.advance (t0, t1, flags);
      return sa;
   }

   /*public void attach(DriverInterface driver) {
      super.attach (driver);
      
      File file = new File(ArtisynthPath.getSrcRelativePath(JawDemo.class,
         "controlpanels/" + "resistance" + ".art"));
      if (file != null) {
         ControlPanel panel = null;
         try {
            panel = (ControlPanel) ComponentUtils.loadComponent(file, this,
                  ControlPanel.class);
         } catch (Exception e) {
            System.out.println(
               "Error reading control panel file "+file+": "+e.getMessage());
         }
         if (panel != null) {
            
            this.addControlPanel(panel);
         }
      }
      
   }*/
   
}
