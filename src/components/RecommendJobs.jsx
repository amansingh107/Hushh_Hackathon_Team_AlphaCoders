import React, { useState } from "react";
import { useUser } from "../UserContext";

export default function RecommendJobs() {
  const { userId } = useUser();
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRecommend = async () => {
    setJobs([]);
    setError("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("user_id", userId);

      const res = await fetch("http://localhost:8000/recommend_jobs/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to fetch jobs");
      }

      const data = await res.json();
      setJobs(data.recommended_jobs || []);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recommend-jobs">
      <button onClick={handleRecommend} disabled={loading}>
        {loading ? "Loading..." : "🔍 Recommend Jobs"}
      </button>

      {error && <div className="error-box">❌ {error}</div>}

      {jobs.length > 0 && (
        <div className="job-list">
          <h3>🎯 Recommended Jobs</h3>
          {jobs.map((job, index) => (
            <div key={index} className="job-card">
              <h4>{job.title}</h4>
              <p>
                <strong>Company:</strong> {job.company}
              </p>
              <p>
                <strong>Location:</strong> {job.location}
              </p>
              <p>
                <strong>Source:</strong> {job.source}
              </p>
              <a href={job.url} target="_blank" rel="noopener noreferrer">
                View Job ↗️
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
