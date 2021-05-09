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
   // keep a list of previous incisor positions
   ArrayList<Point3d> movementHistory = new ArrayList<Point3d>();
   
   // lower incisor at teeth occlusion
   Point3d liInit = new Point3d(0, -47.9584, 41.7642);
   
   // inc describes whether muscle activation is currently incrementing
   boolean inc = true;
   
   public enum TrainingType {
      // increment steps can be adjusted 
      OPENING("opening", 2, -1, 50),
      LEFT_LATEROTRUSION("llat", 0, 1, 10),
      RIGHT_LATEROTRUSION("rlat", 0, -1, 10);
      
      // type of training
      String trainingName;
      // axis and sign together determine the direction of the resistance
      // axis along which the force acts, 0 for x-axis, and 2 for z-axis
      int axis;
      // direction of force along the axis, 1 for positive and -1 for negative direction of axis
      int sign;
      // increment step of the force (in 1/1000N)
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
      
      //System.out.println("displ_dist: " + displ_dist);
           
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
            
            // System.out.println("set force to " + force.getMagnitude ()/1000 + " N");
            
         } else { 
           movementState = MovementState.MOVEMENT_BACK;
           double mag = force.getMagnitude ();
           force.setMagnitude (mag-incSize > 0 ? mag-incSize : 0);
         }   
         
      }
      
      // show force
      force.setAxisLength (force.getMagnitude ()/100);
      
      String muscle = "";
      double excitation = 0;
      
      // depending on the trainingType, perform the corresponding movement
      // by activating, then deactivating, the corresponding muscles
      switch(trainingType) {
         case OPENING:
            muscle = "exciters/bi_open";
            excitation = (double) myJawModel.getProperty (muscle + ":excitation").get ();
            break;
         case LEFT_LATEROTRUSION:
            //small opener excitation for a more stable laterotrusion
            myJawModel.getProperty ("exciters/bi_open:excitation").set (0.005);
            muscle = "axialSprings/rip";
            excitation = (double) myJawModel.getProperty (muscle + ":excitation").get ();
            break;
         case RIGHT_LATEROTRUSION:
          //small opener excitation for a more stable laterotrusion
            myJawModel.getProperty ("exciters/bi_open:excitation").set (0.005);
            muscle = "axialSprings/lip";
            excitation = (double) myJawModel.getProperty (muscle + ":excitation").get ();
            break;
          default: // no muscle activation            
      }
      
      if(excitation >= 1.0){
         inc = false;
      }
      if(inc) {
         myJawModel.getProperty (muscle + ":excitation").set (excitation+0.0025);
      } else if(excitation > 0.0){
         myJawModel.getProperty (muscle + ":excitation").set (excitation-0.005);
      }
      
      StepAdjustment sa = super.advance (t0, t1, flags);
      return sa;
   }
   
}
