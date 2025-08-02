import { useUser } from "../UserContext";
import { useState } from "react";

export default function AnalyzeSkillGap() {
  const { userId } = useUser();
  const [jobTitle, setJobTitle] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("job_title", jobTitle);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze_skill_gap/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const error = await res.text();
        throw new Error(error);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("❌ Error:", err);
      alert("Error analyzing skill gap");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <label>Job Title:</label>
      <input
        value={jobTitle}
        onChange={(e) => setJobTitle(e.target.value)}
        style={{ marginRight: "10px", padding: "6px" }}
      />
      <button onClick={handleAnalyze} style={{ padding: "6px 12px" }}>
        {loading ? "Analyzing..." : "Analyze Skill Gap"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>🔍 Analysis Result</h3>

          <div>
            <strong>User Skills:</strong>
            <ul>
              {result.user_skills.map((skill, index) => (
                <li key={`user-skill-${index}`}>{skill}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Job Required Skills:</strong>
            <ul>
              {result.job_required_skills.map((skill, index) => (
                <li key={`job-skill-${index}`}>{skill}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Skill Gaps:</strong>
            <ul>
              {result.skill_gaps.map((gap, index) => (
                <li key={`skill-gap-${index}`} style={{ color: "red" }}>
                  {gap}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
