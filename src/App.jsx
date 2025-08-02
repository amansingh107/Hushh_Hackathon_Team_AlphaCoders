import { useUser } from "./UserContext";
import './App.css';
import UploadLinkedIn from './components/UploadLinkedIn';
import UploadResume from './components/UploadResume';
import ParseGithub from './components/ParseGithub';
import AnalyzeSkillGap from './components/AnalyzeSkillGap';
import RecommendJobs from './components/RecommendJobs';
import React from 'react';

export default function App() {
  const { userId, setUserId } = useUser();

  return (
    <div className="app-container">
      <div className="form-card">
        <h1 className="form-title">🚀 Career Growth Assistant</h1>
        <p className="form-subtitle">Please upload <strong>at least one</strong> of the following: Resume, LinkedIn archive, or GitHub username to get started.</p>

        <div className="form-group">
          <label htmlFor="userId">👤 User ID</label>
          <input
            id="userId"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter your user ID"
          />
        </div>

        <div className="upload-section">
          <UploadResume userId={userId} />
          <UploadLinkedIn userId={userId} />
          <ParseGithub userId={userId} />
        </div>

        <hr className="divider" />

        <div className="action-section">
          <AnalyzeSkillGap userId={userId} />
          <RecommendJobs userId={userId} />
        </div>
      </div>
    </div>
  );
}
