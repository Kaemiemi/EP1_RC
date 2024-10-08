import java.io.*;
import java.net.*;
import java.util.*;

public class PollServer {
    private static final int PORT = 12345;
    private static Map<Integer, Poll> polls = new HashMap<>();
    private static int pollIdCounter = 1;

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Servidor de enquetes iniciado...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                new ClientHandler(clientSocket).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Classe para gerenciar as conexões de clientes
    private static class ClientHandler extends Thread {
        private Socket clientSocket;

        public ClientHandler(Socket socket) {
            this.clientSocket = socket;
        }

        @Override
        public void run() {
            try (
                BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)
            ) {
                String clientRequest;

                while ((clientRequest = in.readLine()) != null) {
                    System.out.println("Recebido: " + clientRequest);
                    // Processar a solicitação do cliente
                    String response = processRequest(clientRequest);
                    out.println(response);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        // Processa as requisições dos clientes
        private String processRequest(String request) {
            String[] parts = request.split(" ");
            String command = parts[0];

            switch (command) {
                case "CREATE":
                    return createPoll(parts);
                case "VOTE":
                    return votePoll(parts);
                case "LIST":
                    return listPolls();
                case "RESULTS":
                    return pollResults(parts);
                default:
                    return "Comando inválido!";
            }
        }

        // Método para criar uma nova enquete
        private String createPoll(String[] parts) {
            String question = parts[1];
            Poll poll = new Poll(pollIdCounter++, question);
            polls.put(poll.getId(), poll);
            return "Enquete criada com sucesso! ID: " + poll.getId();
        }

        // Método para votar em uma enquete
        private String votePoll(String[] parts) {
            int pollId = Integer.parseInt(parts[1]);
            if (polls.containsKey(pollId)) {
                polls.get(pollId).vote();
                return "Voto computado na enquete ID: " + pollId;
            } else {
                return "Enquete não encontrada!";
            }
        }

        // Método para listar todas as enquetes
        private String listPolls() {
            StringBuilder response = new StringBuilder("Enquetes disponíveis:\n");
            for (Poll poll : polls.values()) {
                response.append(poll.getId()).append(": ").append(poll.getQuestion()).append("\n");
            }
            return response.toString();
        }

        // Método para exibir resultados de uma enquete
        private String pollResults(String[] parts) {
            int pollId = Integer.parseInt(parts[1]);
            if (polls.containsKey(pollId)) {
                return polls.get(pollId).getResults();
            } else {
                return "Enquete não encontrada!";
            }
        }
    }
}
