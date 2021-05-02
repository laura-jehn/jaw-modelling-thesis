package artisynth.core.opensim.components;

import org.w3c.dom.Element;
import org.w3c.dom.Node;

import maspack.util.Logger;

public class PiecewiseLinearFunctionFactory extends OpenSimObjectFactory<PiecewiseLinearFunction> {

   public PiecewiseLinearFunctionFactory () {
      super (PiecewiseLinearFunction.class);
   }
   
   protected PiecewiseLinearFunctionFactory(Class<? extends PiecewiseLinearFunction> functionClass) {
      super(functionClass);
   }
   
   @Override
   protected boolean parseChildren (PiecewiseLinearFunction comp, Element elem) {
    
      // extract both x and y before populating child
      double[] x = null;
      double[] y = null;
      
      boolean success = true;
      Node child = elem.getFirstChild ();
      while (child != null) {
         if (child.getNodeType () == Node.ELEMENT_NODE) {
           
            String name = getNodeName (child);
            Element celem = (Element)child;
            if ("x".equals(name)) {
               x = parseDoubleArrayValue (celem);
            } else if ("y".equals (name)) {
               y = parseDoubleArrayValue (celem);
            } else {
               // pass up
               boolean csuccess = parseChild (comp, celem);
               if (!csuccess) {
                  Logger.getSystemLogger ().info ("Failed to parse subelement '" + getNodeName(child) 
                     + "' for " + comp.getClass ().getName ());
                  success = false;
               }
            }
         }
         child = child.getNextSibling ();
      }
      
      // set knots if both available
      if (x != null && y != null) {
         comp.set (x, y);
      } else {
         success = false;
      }
      
      return success;
      
   }

}
