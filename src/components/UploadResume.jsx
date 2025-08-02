import { useUser } from "../UserContext";
import { useState } from "react";

export default function UploadResume() {
  const { userId } = useUser();
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setMessage("");
    setError("");

    if (!file || file.type !== "application/pdf") {
      setError("Please upload a valid PDF file.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("user_id", userId);
      formData.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/resume/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Upload failed.");
      }

      const data = await res.json();
      console.log(data);
      setMessage("✅ Resume uploaded and parsed successfully!");
    } catch (err) {
      setError(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <label className="upload-label">Upload Resume (.pdf):</label>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="upload-input"
      />
      <button onClick={handleSubmit} disabled={loading} className="upload-button">
        {loading ? "Uploading..." : "Submit Resume"}
      </button>
      {message && <div className="success-msg">{message}</div>}
      {error && <div className="error-msg">{error}</div>}
    </div>
  );
}
