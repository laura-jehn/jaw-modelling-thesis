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
import maspack.matrix.Point3d;
import maspack.matrix.Vector3d;
import maspack.render.RenderProps;
import maspack.render.Renderer;

public class ResistanceDemo extends JawLarynxDemo {
   
   PointForce myPointForce;
   FrameMarker li;
   ArrayList<Point3d> movementHistory = new ArrayList<Point3d>();
   
   //Point3d liInit = new Point3d(0, -47.9584, 41.7642);
   Point3d liInit = new Point3d(0, -47.51, 35.57);
   
   boolean inc = true;
   
   enum TrainingType {
      OPENING("opening", 2, -1, 0.1), CLOSING("closing", 2, 1, 0.1), LEFT_LATEROTRUSION("llat", 0, 1, 0.05), RIGHT_LATEROTRUSION("rlat", 0, -1, 0.05);
      
      String trainingName;
      int dominantComponent;
      int sign;
      double forcePerDist;
      
      private TrainingType (String trainingName, int dominantComponent, int sign, double forcePerDist) {
         this.trainingName = trainingName;
         this.dominantComponent = dominantComponent;
         this.sign = sign;
         this.forcePerDist = forcePerDist;
      }
      
      public String getTrainingName() {
         return trainingName;
      }

      public int getDominantComponent() {
         return dominantComponent;
      }

      public int getSign() {
         return sign;
      }
      
      public double getForcePerDist() {
         return forcePerDist;
      }
   }

   TrainingType trainingType = TrainingType.OPENING;
   
   enum MovementState {IN_MOVEMENT, AT_LIMIT, MOVEMENT_BACK, IDLE};
   MovementState movementState = MovementState.IDLE;
   
   double forcePerDist = 0.1; // per mm of displacement, increase resistance by 0.1N, so that at 10mm displacement, there will be 1 Newton resistance
   // should probably be adjusted for the different training types
   
   public void build (String[] args) throws IOException {
      super.build (args);
      
      li = (FrameMarker)myJawModel.findComponent ("frameMarkers/lowerincisor");
      myPointForce = new PointForce (li);
      myJawModel.addForceEffector (myPointForce);
      
      RenderProps.setLineStyle (myPointForce, Renderer.LineStyle.CYLINDER);
      RenderProps.setLineRadius (myPointForce, 0.5);
      RenderProps.setLineColor (myPointForce, Color.GREEN);
   }
   
   public StepAdjustment advance (double t0, double t1, int flags) {
      
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
      
      Point3d dir = new Point3d();
      if(movementHistory.size () > 1) {
         dir.sub (movementHistory.get(0), movementHistory.get(noPreviousPoints-1));
      }
      
      double velocity = li.getVelocity ().norm ();
      velocity = dir.norm();
      
      if(velocity < 0.1) {
         System.out.println("jaw is not moving");
         // jaw is not moving
         switch(movementState) {
            case IN_MOVEMENT:
               movementState = MovementState.AT_LIMIT;
               
            case MOVEMENT_BACK:
               movementState = MovementState.IDLE;
            default:
         }
      } else {
         System.out.println("jaw is moving with velocity " + velocity);
         
         // determine direction in which jaw is moving
         
         int i = trainingType.getDominantComponent ();
         int sign = trainingType.getSign ();
         
         System.out.println("direction is " + dir.toString ());
         System.out.println(" z / norm = " + sign * dir.get (i) / dir.norm ());
         System.out.println(" with sign " + sign + " and component " + dir.get (i) + " with norm " + dir.norm ());
         
         if(true) { //-1 * sign * dir.get (i) / dir.norm () > 0.85 ){
            movementState = MovementState.IN_MOVEMENT;
            // the further from inc init, the higher magnitude
            myPointForce.setMagnitude (displ_dist * forcePerDist * 1000);
            System.out.println("set force to " + displ_dist * forcePerDist + " N");
            
            // myPointForce.setDirection (dir);
            Point3d direction = new Point3d();
            direction.set (i, -1 * sign);
            myPointForce.setDirection(direction);
         } //else {
           // movementState = MovementState.MOVEMENT_BACK;
            //myPointForce.setMagnitude (0);
         //}        
      }
      
      myPointForce.setAxisLength (myPointForce.getMagnitude ()/100);
      
      double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
      double closers_excitation = (double) myJawModel.getProperty ("exciters/bi_close:excitation").get ();
      
      switch(trainingType) {
         case OPENING:            
            if(openers_excitation > 0.8){
               inc = false;
            }
            if(inc) {
               myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
            } else if(openers_excitation > 0.0){
               myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation-0.005);
            }
         case CLOSING:
            if(openers_excitation > 0.2){
               inc = false;
            }
            if(inc) {
               myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
            } else if(openers_excitation > 0.0){
               myJawModel.getProperty ("exciters/bi_open:excitation").set (0);
               myJawModel.getProperty ("exciters/bi_close:excitation").set (closers_excitation-0.005);
            }
          default:
            
      }
      
      
      StepAdjustment sa = super.advance (t0, t1, flags);
      return sa;
   }
   
   // eval scenario: test run for opening, closing, laterotrusion where openers/closers/lp are activated to different levels several times (in compromised jaw),
   // plot response of orthosis (forces)
   // progress in gained muscle function cannot be evaluated in the simulation

   public void attach(DriverInterface driver) {
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
      
      addBreakPoint(0.5);
   }
   
}
