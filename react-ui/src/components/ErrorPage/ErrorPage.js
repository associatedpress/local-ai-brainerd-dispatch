
import React, { useState } from 'react';
import './ErrorPage.css';
import Banner from '../Banner/Banner';
import ImageUploader from '../ImageUploader/ImageUploader';
const ErrorPage = ({ errorResponse, file, agencies, session_token, selected_agency }) => {
  const [textareaData, setTextareaData] = useState([]);
  const [filedsData, setFieldsData] = useState(errorResponse.response);
  const [selectedAgency, setSelectedAgency] = useState(selected_agency);
  const [selectedParser, setSelectedParser] = useState("");
  const [isSuccess, setIsSuccess] = useState()
  const [isVisible, setIsVisible] = useState(false);
  const [isBlotterConfigured, setIsBlotterConfigured] = useState(false);
  const [message, setMessage] = useState("");
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;

  const handleTextareaChange = (index, db_label, value) => {
    console.log(db_label)
    const updatedData = [...textareaData];
    updatedData[index] = value;
    console.log(updatedData)
    setTextareaData(updatedData);

    const updatedFielsData = [...filedsData];
    const obj = {db_label:db_label, "parser_label":value, "labeled_correctly": false}
    updatedFielsData[index] = obj;
    console.log(updatedFielsData)
    setFieldsData(updatedFielsData);
  };

  const handleSubmit = (e) => {
    const queryParams = new URLSearchParams();
    queryParams.append('parser_id', selectedParser);
    queryParams.append('agency_id', selectedAgency);
    const url = baseuri + '/updateparsermappings?' + queryParams.toString();
    var obj = {}
    e.preventDefault();
    console.log(filedsData);
    for (const data of filedsData) 
    { 
            console.log(data);
            if(data.labeled_correctly === false)
            {
                obj[data.parser_label] = data.db_label
            }

    }
    console.log(obj)
    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'session-token': session_token
        },
        body: JSON.stringify(obj)
      })
        .then(data => {
            setMessage("Updated the blotter configuration successfully. Parse the blotter again.");
            setIsSuccess(true); // Set isSuccess to false on failure
            setIsVisible(true);
            setIsBlotterConfigured(true);
            // setTimeout(() => {
            //     setIsVisible(false);
            // }, 5000);
        })
        .catch(error => {
            setMessage("Failed to update the blotter configuration. Please check all the fields.");
            setIsSuccess(false); // Set isSuccess to false on failure
            setIsVisible(true);
        });

  };

  const handleBannerClose = () => {
    setIsVisible(false);
  };

  function handleAgencyChange(event) {
    setSelectedAgency(event.target.value);
  }

  function handleParserChange(event) {
    setSelectedParser(event.target.value);
  }

  return (
    <div className="error-page-container">
      {isBlotterConfigured ? (
        <ImageUploader  file={file} agencies={agencies} session_token = {session_token} selected_agency = {selectedAgency} show_preview = {true}/> // Render the ErrorPage component if isError is true
      ) : (
      <div className="both-box">
                <div className="error-image-box">
                   <h4 className="error-image-title">Change Blotter Configuration</h4>
                    <div>
                   <select className="error-agencyDropdown" value={selectedAgency} onChange={handleAgencyChange}>
                       <option value="">Select an agency</option>
                      {agencies.map((agency) => (
                        <option key={agency.agency_id} value={agency.agency_id}>
                            {agency.agency_name}
                        </option>
                        ))}
                    </select>


                    <select className="error-ParserDropdown" value={selectedParser} onChange={handleParserChange}>
                       <option value="">Select a parser</option>
                      {agencies.map((agency) => (
                        <option key={agency.agency_id} value={agency.agency_id}>
                            {agency.agency_name}
                        </option>
                        ))}
                    </select>
                    </div>
                    {file && (
                        <div className="error-uploaded-image-container">
                            {file.type === 'application/pdf' ? (
                                <object
                                    data={URL.createObjectURL(file)}
                                    type="application/pdf"
                                    width="100%"
                                    height="100%"
                                >
                                    <p>
                                        Your browser does not support PDFs.
                                        <a href={URL.createObjectURL(file)}>Click here to download the PDF file.</a>
                                    </p>
                                </object>
                            ) : (
                                <img src={URL.createObjectURL(file)} alt="Uploaded file" className="uploaded-image" />
                            )}
                        </div>
                    )}
                </div>
        <div className="error-message-box">
          <h4 className="error-message-title">Match Category Names</h4>
          <div className="error-response">
            {errorResponse.response.map((item, index) => (
              <div key={index}>
                <p className="db_label">{item.db_label}</p>
                <textarea
                  defaultValue={item.parser_label}
                  onChange={(e) => handleTextareaChange(index,item.db_label, e.target.value)}
                />
              </div>
            ))}
          </div>
          <button className="error-uploadBtn" onClick={handleSubmit}>
            Submit
          </button>
          {isVisible && <Banner message={message} isVisible={isVisible} isSuccess = {isSuccess} onClose={handleBannerClose}></Banner>}
        </div>
      </div> )}
    </div>
  );
};

export default ErrorPage;
