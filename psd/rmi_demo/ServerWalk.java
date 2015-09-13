import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class ServerWalk {
	
	public static void main(String[] args) {
		try {
			Walk awalk = new Walk();
			Registry r = LocateRegistry.createRegistry(Registry.REGISTRY_PORT);
			String objname = "walkserver";
			System.out.println("registrando " +objname+ "...");
			r.rebind(objname, awalk);
			System.out.println("registrado!");
		}
		catch (Exception e) {
			System.err.println("erro na main()! " + e);
			e.printStackTrace();
			System.exit(2);
		}
		System.out.println("esperando requisicao...");
	} 
}