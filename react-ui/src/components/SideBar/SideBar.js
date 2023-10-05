import React, { useState, useEffect } from 'react';
import './SideBar.css'

const SideBar = ({ onHomeClick, onUploadClick, publishedClick, ignoredClick, onPublishClick, onCategoryClick, onSettingsClick }) => {


  const [publications, setPublications] = useState([]);
  const [selectedPublication, setSelectedPublication] = useState();
  const [session_token, setSessionToken] = useState(localStorage.getItem('session_token'));
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;

  useEffect(() => {
    console.log("Side bar")
    console.log(session_token)
    // console.log("ImageUploader mounted");

    fetch(baseuri + `/publications`, {
      headers: {
        "session-token": session_token
      }
    })
      .then((response) => response.json())
      .then((data) => {
        setPublications(data.response);
        setSelectedPublication(1);
        localStorage.setItem('selected_publication', 1);
      })
      .catch((error) => {
        console.error("Error fetching publication data:", error);
      });
  }, []);

  const handleImageUploaderClick = () => {
    onUploadClick();
    console.log("Button clicked: ");

  }

  const handlePublishNewReportsClick = () => {
    onPublishClick();
  }

  const handlePublishedReportsClick = () => {
    publishedClick();
  }

  const handleIgnoredReportsClick = () => {
    ignoredClick();
  }

  const handleHomeClick = () => {
    onHomeClick();
  }

  const handleCategoryClick = () => {
    onCategoryClick();
  }

  const handleSettingsClick = () => {
    onSettingsClick();
  }

  function handlePublicationChange(event) {
    setSelectedPublication(event.target.value);
    localStorage.setItem('selected_publication', event.target.value);
  }


  return (
    <div className="sidebar">
      <button className="btn" onClick={handleHomeClick}>Home</button>
      <button className="btn" onClick={handleImageUploaderClick}>Upload</button>
      <button className="btn" onClick={handlePublishNewReportsClick}>Publish New Report</button>
      <button className="btn" onClick={handlePublishedReportsClick}>Published Reports</button>
      <button className="btn" onClick={handleIgnoredReportsClick}>Ignored Reports</button>
      <button className="btn" onClick={handleCategoryClick}>Category Maintenance</button>
      <div className="publication-box">
          <h3 className="agencyTitle">
            Select Publication
          </h3>
          <select className="agencyDropdown" value={selectedPublication} onChange={handlePublicationChange}>
            <option value="">Select Publication</option>
            {publications.map((publication) => (
              <option key={publication.publication_id} value={publication.publication_id}>
                {publication.publication_name}
              </option>
            ))}
          </select>
        </div>
        <button className="btn" onClick={handleSettingsClick} id="settingsBtn">Settings</button>
    </div>
    
  );
};

export default SideBar;