import { useUser } from "../UserContext";
import { useState } from "react";

export default function ParseGithub() {
  const { userId } = useUser();
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setMessage("");
    setError("");

    if (!username.trim()) {
      setError("Please enter your GitHub username.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("user_id", userId);
      formData.append("github_username", username);

      const res = await fetch("http://localhost:8000/parse_github/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "GitHub parsing failed.");
      }

      const data = await res.json();
      console.log(data);
      setMessage("✅ GitHub profile parsed successfully!");
    } catch (err) {
      setError(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <label className="upload-label">GitHub Username:</label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter GitHub username"
        className="upload-input"
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="upload-button"
      >
        {loading ? "Submitting..." : "Submit GitHub"}
      </button>
      {message && <div className="success-msg">{message}</div>}
      {error && <div className="error-msg">{error}</div>}
    </div>
  );
}
