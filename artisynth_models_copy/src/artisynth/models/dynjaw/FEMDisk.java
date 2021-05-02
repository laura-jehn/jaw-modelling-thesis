package artisynth.models.dynjaw;

import artisynth.core.femmodels.FemModel3d;
import artisynth.core.femmodels.FemNode3d;
import artisynth.core.materials.LigamentAxialMaterial;
import artisynth.core.materials.MooneyRivlinMaterial;
import artisynth.core.mechmodels.FrameMarker;
import artisynth.core.mechmodels.MechSystemSolver.Integrator;
import artisynth.core.mechmodels.MultiPointMuscle;
import artisynth.core.mechmodels.MultiPointSpring;
import artisynth.core.mechmodels.Particle;
import artisynth.core.mechmodels.RigidBody;
import artisynth.core.mechmodels.RigidCylinder;
import artisynth.core.modelbase.StepAdjustment;

import java.awt.Color;
import java.io.IOException;
import java.util.ArrayList;

import artisynth.core.femmodels.FemFactory;
import artisynth.core.femmodels.FemMarker;
import artisynth.core.femmodels.FemModel.SurfaceRender;
import maspack.geometry.PolygonalMesh;
import maspack.matrix.Point3d;
import maspack.matrix.RigidTransform3d;
import maspack.properties.Property;
import maspack.render.RenderProps;
import maspack.render.GL.GLViewer;

/* FEMDisk extends the jaw model with the articular disk in the TMJ */
public class FEMDisk extends JawDemo {
   
   FemModel3d disk;
   double diskWeight = 0.0006; // weight in kg (0.6g)
   
   // cylinder for making anterior ligament wrap around the condyle
   RigidBody cylinder;
   // lateral ligament
   MultiPointSpring llSpr;
   // medial ligament
   MultiPointSpring mlSpr;
   // anterior ligament
   MultiPointSpring alSpr = new MultiPointSpring();
   // posterior ligament
   MultiPointSpring plSpr;
   ArrayList<MultiPointSpring> springs = new ArrayList<>();
   
   double[] maximumLengths = {2.5, 4, 1.9, 7.5}; // maximum ligament lengths as defined by Sagl
   
   // inc describes whether mouth opening muscle activation is currently incrementing
   boolean inc = true;
   
   
   
   public void build(String[] args) throws IOException {
      super.build(args);
      
      myJawModel.setIntegrator (Integrator.ConstrainedBackwardEuler);
      myJawModel.setMaxStepSize (0.001);
      
      // create and add FemModel
      disk = new FemModel3d ("disk");
      myJawModel.add (disk);
      
      PolygonalMesh condyleSurface = new PolygonalMesh("condyleSurface.obj");
      int layers = 4;         // no. of layers  
      double thickness = 0.2;  // layer thickness
      double offset = 0.1;  // center the layers about the surface
      // create extrusion from condyle surface mesh
      FemFactory.createExtrusion( disk, layers, thickness, offset, condyleSurface );
            
      // set FEM material properties
      MooneyRivlinMaterial mat = new MooneyRivlinMaterial();
      mat.setC10 (9e5/1000); // convert Pa to mPa
      mat.setC01 (9e2/1000);
      disk.setStiffnessDamping (1.0);
      disk.setMaterial (mat);
      
      disk.setSurfaceRendering (SurfaceRender.Stress);
      
      disk.updateVolume ();
      double density = diskWeight / disk.getVolume ();
      disk.setDensity (density);
      // System.out.println("density: " + density);
      // System.out.println("volume: " + disk.getVolume ());
      
      // get jaw and maxilla position from jaw model
      RigidBody jaw = myJawModel.rigidBodies ().get ("jaw");
      RigidBody maxilla = myJawModel.rigidBodies ().get ("maxilla");
      RenderProps.setVisible (maxilla, true);
      
      myJawModel.setCollisionBehavior (disk, jaw, true);
      myJawModel.setCollisionBehavior (disk, maxilla, true);
      
      Point3d ltmj_pos = myJawModel.frameMarkers ().get ("ltmj").getPosition ();
      // the ltmj position (centre of left condyle) is used to position the ligaments
      double ltmj_x = ltmj_pos.x;
      double ltmj_y = ltmj_pos.y;
      double ltmj_z = ltmj_pos.z;
      
      
      // create wrapping cylinder
      cylinder = new RigidCylinder ("wrapSurface", /*rad=*/4, /*h=*/8, /*density=*/0, /*nsegs=*/32);
      cylinder.setPose (new RigidTransform3d(ltmj_x+4, ltmj_y, ltmj_z, 0, 90, 0));
      myJawModel.addRigidBody (cylinder);
      myJawModel.attachFrame (cylinder, jaw);
      RenderProps.setVisible (cylinder, false);
         
      // set rendering properties
      setRenderProps ();
      
      // add ligaments to hold disk in place
      // for each ligament, a Particle is created for attaching one end of the ligament to the jaw or maxilla
      // a FemMarker is created for attaching the other end of the ligament to the FEM disk
      
      // Lateral Ligament (outside)
      Particle ll = new Particle("ll", .1, ltmj_x+8, ltmj_y, ltmj_z);
      FemMarker llMkr = new FemMarker(ltmj_x+8, ltmj_y, ltmj_z+2);
      llSpr = addLigament(ll, jaw, llMkr);
      
      // Medial Ligament (inside)
      Particle ml = new Particle("ml", .1, ltmj_x-8, ltmj_y, ltmj_z);
      FemMarker mlMkr = new FemMarker(ltmj_x-4, ltmj_y, ltmj_z+3.5);
      mlSpr = addLigament(ml, jaw, mlMkr);
      
      // Anterior Ligament
      Particle al = new Particle("al", .1, ltmj_x+4, ltmj_y-4, ltmj_z);
      FemMarker alMkr = new FemMarker(ltmj_x+4, ltmj_y-2.5, ltmj_z+3.5);
      alSpr = addLigament(al, jaw, alMkr);
      
      // Posterior Ligament
      Particle pl = new Particle("pl", .1, ltmj_x, ltmj_y+4, ltmj_z+6);
      FemMarker plMkr = new FemMarker(ltmj_x, ltmj_y+4, ltmj_z+4);
      plSpr = addLigament(pl, maxilla, plMkr);
      
      // add springs to a list
      springs.add (llSpr);
      springs.add (alSpr);
      springs.add (mlSpr);
      springs.add (plSpr); 
   }
   
   public MultiPointSpring addLigament(Particle p, RigidBody body, FemMarker mkr) {
      
      MultiPointMuscle spr = MultiPointMuscle.createLinear ();
      LigamentAxialMaterial mat = new LigamentAxialMaterial();
      mat.setDamping (0.005);
      spr.setMaterial (mat);
      
      myJawModel.addParticle(p);
      myJawModel.attachPoint(p, body);
      myJawModel.add (spr);
      disk.addMarker (mkr);
      
      // attach closest FEM nodes to FemMarker so that force of ligament will be distributed across several nodes
      double attachmentRadius = 1.0;
      ArrayList<FemNode3d> nodes = disk.findNearestNodes(mkr.getPosition (), attachmentRadius);
      System.out.println(nodes.size ());
      mkr.setFromNodes (nodes);
      
      spr.addPoint (p); // start of ligament is the particle attached to maxilla/jaw
      
      // in case of anterior ligament, add wrapping cylinder
      if(p.getName ().equals ("al")) {
         spr.setSegmentWrappable (50);
         spr.addPoint (mkr);
         spr.addWrappable (cylinder);
         spr.updateWrapSegments ();
      } else {
         spr.addPoint (mkr);
      }
      
      spr.setRestLengthFromPoints ();
      
      // set render properties
      for (FemNode3d n : nodes) {
         RenderProps.setSphericalPoints (n,  0.07,  Color.GREEN);
      }
      RenderProps.setCylindricalLines (spr, 0.5, Color.GREEN);
      RenderProps.setPointRadius (p, 0.7);
      
      return spr;
   }
   
   // sets the FEMs render properties
   protected void setRenderProps () {
      RenderProps.setLineColor (disk, Color.blue);
      RenderProps.setLineRadius (disk, 0.0001);
      RenderProps.setLineWidth (disk, 0);
      RenderProps.setPointRadius (disk, 0.0);     
   }
   
   public StepAdjustment advance (double t0, double t1, int flags) {
      
      // check whether length of spring has reached maximum length
      // if so, increase elongation stiffness of the spring
      for(int i=0; i<4; i++) {
         MultiPointSpring spr = springs.get (i);
         if(spr.getLength () > spr.getRestLength() + maximumLengths[i]) {
            LigamentAxialMaterial mat = (LigamentAxialMaterial) spr.getMaterial ();
            mat.setElongStiffness (0.25);
         }
      }
      
      // perform opening movement
      Property excitation_property = myJawModel.getProperty ("exciters/bi_open:excitation");
      double openers_excitation = (double) excitation_property.get ();
      if(openers_excitation >= 0.15) {
         // stop incrementing opening muscle activation
         inc = false;
      }
      if(inc) {
         excitation_property.set (openers_excitation+0.005);
      } else if(openers_excitation > 0.005){
         excitation_property.set (openers_excitation-0.005);
      }
      
      /*GLViewer viewer = getMainViewer();
      viewer.setOrthographicView (true);
      setViewerCenter (new Point3d (00, 40, 80.0));
      setViewerEye (new Point3d (500.0, 0, 80.0));
      viewer.zoom (0.35);*/
      
      return super.advance(t0, t1, flags);
   }
   
}
