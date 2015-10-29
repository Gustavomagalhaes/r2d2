import java.rmi.Naming;
import java.rmi.RemoteException;

public class ClientWalk {
	
	public static void main(String[] args) {
		
		IWalk rwalk = null;
		
		try {
			String objname =  "rmi://localhost/walkserver";
			System.out.println("Procurando pelo objeto " + objname);
			rwalk = (IWalk) Naming.lookup(objname);
		}
		catch (Exception e) {
			System.err.println("Problemas ao executar o lookup! " + e);
			e.printStackTrace();
			System.exit(2);
		}
		try {
			int n = 5;
			String resp = null;
			resp = rwalk.total();
			System.out.println("Resposta recebida:\n\t" + resp);
			rwalk.move(n);
			resp = rwalk.total();
			System.out.println("Resposta recebida:\n\t" + resp);
		}
		catch (RemoteException re) {
			System.err.println("Problemas durante chamada remota! " + re);
			re.printStackTrace();
			System.exit(3);
		}
	}
}