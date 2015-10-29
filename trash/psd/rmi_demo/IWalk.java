import java.rmi.Remote;
import java.rmi.RemoteException;

public interface IWalk extends Remote
{
	void move(int n) throws RemoteException;
	String total() throws RemoteException;
}