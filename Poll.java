public class Poll {
    private int id;
    private String question;
    private int votes;

    public Poll(int id, String question) {
        this.id = id;
        this.question = question;
        this.votes = 0;
    }

    public int getId() {
        return id;
    }

    public String getQuestion() {
        return question;
    }

    public void vote() {
        this.votes++;
    }

    public String getResults() {
        return "Enquete: " + question + " | Votos: " + votes;
    }
}
