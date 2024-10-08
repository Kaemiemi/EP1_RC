import java.io.*;
import java.net.*;

public class PollClient {
    private static final String SERVER_ADDRESS = "localhost";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        try (Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in))) {

            String userInput;

            System.out.println("Conectado ao servidor de enquetes.");
            System.out.println("Digite um comando (CREATE, VOTE, LIST, RESULTS):");

            while ((userInput = stdIn.readLine()) != null) {
                out.println(userInput);
                String response = in.readLine();
                System.out.println("Servidor: " + response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
