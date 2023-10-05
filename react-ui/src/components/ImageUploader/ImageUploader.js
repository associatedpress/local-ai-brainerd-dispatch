import React, { useState, useEffect } from 'react';
import './ImageUploader.css';
import ErrorPage from '../ErrorPage/ErrorPage';
import Banner from '../Banner/Banner';


const ImageUploader = (props) => {
  const [session_token, setSessionToken] = useState(localStorage.getItem('session_token'));
  const [file, setFile] = useState(props.file);
  const [agencies, setAgencies] = useState([]);
  const [selectedAgency, setSelectedAgency] = useState(props.selected_agency);
  const [showPreview, setShowPreview] = useState(props.show_preview); // Add new state variable
  const [isSuccess, setIsSuccess] = useState()
  const [isVisible, setIsVisible] = useState(false);
  const [message, setMessage] = useState("");
  const [errorResponse, setErrorResponse] = useState("");
  const [isError, setIsError] = useState(false); // Add a state variable to track error status

  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;

  useEffect(() => {
    console.log("Image Uploader")
    console.log(session_token)
    // console.log("ImageUploader mounted");

    fetch(baseuri + `/agencies`, {
      // fetch(`/agencies`, {
      headers: {
        "session-token": session_token
      }
    })
      .then((response) => response.json())
      .then((data) => {
        setAgencies(data.response);
      })
      .catch((error) => {
        console.error("Error fetching agency data:", error);
      });
  }, []);

  // useEffect(() => {
  //   console.log("ImageUploader re-rendered");
  // });

  function handleAgencyChange(event) {
    setSelectedAgency(event.target.value);
  }

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
    setShowPreview(true); // Set showPreview to true when a file is selected
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const selectedFile = event.dataTransfer.files[0];
    setFile(selectedFile);
    setShowPreview(true); // Set showPreview to true when a file is selected
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('agency', selectedAgency);
    console.log("Image uploader")
    fetch(baseuri +`/process_blotters`, {
      method: 'POST',
      headers: {
        "session-token": session_token
      },
      body: formData
    })
      .then(response => {
        setShowPreview(false);
        if (response.ok) {
          setMessage("Upload Successful. Blotter file is being processed.");
          setIsVisible(true);
          setIsSuccess(true); // Set isSuccess to true on success
          setTimeout(() => {
            setIsVisible(false);
          }, 5000);
        } else if (response.status === 500) {
          response.json().then(data => {
            setMessage("Upload Failed. Please check the blotter configuration.");
            setIsVisible(true);
            setIsSuccess(false); 
            // Below parameters are set only when selfservice implementation is needed for the system
            // setErrorResponse(data); 
            // setIsError(true);
            
          });
        } else {
          setMessage("Upload Failed. Please check the file formats and request structure.");
          setIsVisible(true);
          setIsSuccess(false); // Set isSuccess to false on failure
        }
      })
      .catch(error => {
        setMessage("Unable to send the request to server.");
        setIsVisible(true);
        setIsSuccess(false);
      });
  };
  
  const handleBannerClose = () => {
    setIsVisible(false);
  };

  return (
    <div className="container">
      {isError ? (
        <ErrorPage errorResponse={errorResponse} file={file} agencies={agencies} session_token = {session_token} selected_agency = {selectedAgency}/> // Render the ErrorPage component if isError is true
      ) : (
      <div className="box">
        <div className="box1">
          <h3 className="agencyTitle">
            Select Reporting Agency
          </h3>
          <select className="agencyDropdown" value={selectedAgency} onChange={handleAgencyChange}>
            <option value="">Select an agency</option>
            {agencies.map((agency) => (
              <option key={agency.agency_id} value={agency.agency_id}>
                {agency.agency_name}
              </option>
            ))}
          </select>
        </div>
        <div className="box2">
          <h3 className="fileTitle">
            Upload Blotter File
          </h3>
          <div className="image-uploader-container" onDragOver={handleDragOver} onDrop={handleDrop}>
            <div className="image-upload-box">
              <label htmlFor="fileUpload">Choose file:</label>
              <input type="file" id="fileUpload" onChange={handleFileChange} accept=".jpg,.jpeg,.png,.pdf" />
            </div>
            <div className="image-upload-box">
              <label htmlFor="fileUpload">Choose file:</label>
              <input type="file" id="fileUpload" onChange={handleFileChange} accept=".jpg,.jpeg,.png,.pdf" style={{ display: 'none' }} />
            </div>
            <div className="upload-area" onDragOver={handleDragOver} onDrop={handleDrop} onClick={() => document.getElementById('fileUpload').click()}>
              <span>Drop file into this space or click to select a local file</span>
              {showPreview && file && (
                <div className="file-preview-container">
                  {file.type === "application/pdf" ? (
                    <object
                      data={URL.createObjectURL(file)}
                      type="application/pdf"
                      width="100%"
                      height="100%"
                    >
                      <p>
                        Your browser does not support PDFs.
                        <a href={URL.createObjectURL(file)}>Click here to download the file.</a>
                      </p>
                    </object>
                  ) : (
                    <img src={URL.createObjectURL(file)} alt="Uploaded file" className="file-preview" />
                  )}
                </div>
              )}
            </div>
          </div>
          <button className="uploadBtn" onClick={handleUpload} disabled={!selectedAgency || !file || !showPreview}>
            Upload </button>
          {isVisible && <Banner message={message} isVisible={isVisible} isSuccess = {isSuccess} onClose={handleBannerClose}></Banner>}
        </div>
      </div>
      )}
    </div>
  );
};

export default ImageUploader;

