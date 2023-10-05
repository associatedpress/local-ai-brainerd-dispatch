import React, { useState, useEffect } from "react";
import "./PublishNewReports.css";
import Banner from '../Banner/Banner';

function PublishNewReports(props) {
  //console.log('Session token:', props.session_token);
  var session_token = localStorage.getItem('session_token');
  const [selectedRows, setSelectedRows] = useState([]);
  const [rows, setRows] = useState([]);
  const [isSuccess, setIsSuccess] = useState()
  const [isVisible, setIsVisible] = useState(false);
  const [message, setMessage] = useState("");
  const [sortOrder, setSortOrder] = useState("asc");
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;


  useEffect(() => {
    fetchPublishedReports()
  }, []);

  function fetchPublishedReports() {
    fetch(baseuri + `/getunpublishedreports`, {
      headers: {
        "session-token": session_token
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.response)
        data = data.response
        const updatedRows = data.map(row => ({ ...row, selected: false }));
        setRows(updatedRows);
      })
      .catch(error => console.error('Error fetching unpublished reports:', error));
  }

  const handleRowClick = (id) => {
    setRows((prevRows) =>
      prevRows.map((row) => {
        if (row.cid === id) {
          console.log({ ...row, selected: !row.selected })
          return { ...row, selected: !row.selected };
        } else {
          return row;
        }
      })
    );
  };

  const handleSelectAll = () => {
    const updatedRows = rows.map((row) => {
      return { ...row, selected: true };
    });
    setRows(updatedRows);
    setSelectedRows(updatedRows.map((row) => row.id));
  };

  const handleSelectNone = () => {
    const updatedRows = rows.map((row) => {
      return { ...row, selected: false };
    });
    setRows(updatedRows);
    setSelectedRows([]);
  };

  const handleSelect24Hours = () => {
    const updatedRows = rows.map((row) => {
      return { ...row, selected: false };
    });

    setRows(updatedRows);
    setSelectedRows([]);

    const now = new Date();
    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);

    const filteredRows = rows.filter((row) => {
      const rowDateTime = new Date(row.dateTime);
      return rowDateTime > yesterday && rowDateTime <= now;
    });

    const rowIds = filteredRows.map((row) => row.id);

    setRows((prevRows) =>
      prevRows.map((row) => {
        if (rowIds.includes(row.id)) {
          return { ...row, selected: true };
        } else {
          return row;
        }
      })
    );
  };
  const handleSelect48Hours = () => {
    const updatedRows = rows.map((row) => {
      return { ...row, selected: false };
    });

    setRows(updatedRows);
    setSelectedRows([]);

    const now = new Date();
    const dayBeforeYesterday = new Date(now)
    dayBeforeYesterday.setDate(dayBeforeYesterday.getDate() - 2);

    const filteredRows = rows.filter((row) => {
      const rowDateTime = new Date(row.dateTime);
      return rowDateTime > dayBeforeYesterday && rowDateTime <= now;
    });

    const rowIds = filteredRows.map((row) => row.id);

    setRows((prevRows) =>
      prevRows.map((row) =>
        rowIds.includes(row.id) ? { ...row, selected: true } : row
      )
    );
    setSelectedRows(rowIds);
  };
  const handleSelectLast7Days = () => {
    const updatedRows = rows.map((row) => {
      return { ...row, selected: false };
    });

    setRows(updatedRows);
    setSelectedRows([]);

    const now = new Date();
    const weekAgo = new Date(now);
    weekAgo.setDate(weekAgo.getDate() - 7);

    const filteredRows = rows.filter((row) => {
      const rowDateTime = new Date(row.dateTime);
      return rowDateTime > weekAgo && rowDateTime <= now;
    });

    const rowIds = filteredRows.map((row) => row.id);

    setRows((prevRows) =>
      prevRows.map((row) =>
        rowIds.includes(row.id) ? { ...row, selected: true } : row
      )
    );
    setSelectedRows(rowIds);
  };

  const handlePublish = () => {
    const selectedIds = rows.filter((row) => row.selected).map((row) => row.cid);
    if (selectedIds.length <= 0)
        return ;
    console.log(selectedIds)
    fetch(baseuri + `/publishreports`, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'session-token': session_token
      },
      body: JSON.stringify({ case_ids: selectedIds })
    })
      .then(response => {
        console.log('Publish success:', response.json());
        if (response.ok) {
          setMessage("Blotter items published to vendor for story generation.");
          setIsVisible(true);
          setIsSuccess(true); // Set isSuccess to true on success
          setTimeout(() => {
            setIsVisible(false);
          }, 5000);
          fetchPublishedReports();
        } else {
          setMessage("Unable to publish the blotter items to vendor.");
          setIsSuccess(false); // Set isSuccess to false on failure
          setIsVisible(true);
        }
      })
      .catch(error => {
        console.error('Publish error:', error);
        setMessage("Unable to send the request to server.");
        setIsVisible(true);
        setIsSuccess(false);
      });
  };


  const handleIgnore = () => {
    const selectedIds = rows.filter((row) => row.selected).map((row) => row.cid);
    if (selectedIds.length <= 0)
        return ;
    console.log(selectedIds)
    fetch(baseuri + `/ignorecases`, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'session-token': session_token
      },
      body: JSON.stringify({ case_ids: selectedIds })
    })
      .then(response => {
        console.log('Added items to ignore list : ', response.json());
        if (response.ok) {
          setMessage("Selected items added to ignore list.");
          setIsVisible(true);
          setIsSuccess(true); // Set isSuccess to true on success
          setTimeout(() => {
            setIsVisible(false);
          }, 5000);
          fetchPublishedReports();
        } else {
          setMessage("Unable to add items to ignore list.");
          setIsSuccess(false); // Set isSuccess to false on failure
          setIsVisible(true);
        }
      })
      .catch(error => {
        console.error('Publish error:', error);
        setMessage("Unable to send the request to server.");
        setIsVisible(true);
        setIsSuccess(false);
      });
  };

  const isSelected = () => {
    const selectedIds = rows.filter((row) => row.selected).map((row) => row.cid);
    if (selectedIds.length > 0)
        return true;
    else 
        return false;
  };

  const handleBannerClose = () => {
    setIsVisible(false);
  };

  return (
    <div className="main-container">
      <div className="main-box">
        <div className="main-box1">
          <h4 className="blotterItems">Review Blotter Items</h4>
          <div className="buttonContainer">
            <button className="reportsBtn" onClick={handleSelectAll}>Select All</button>
            <button className="reportsBtn" onClick={handleSelect24Hours}>Select All From Last 24 Hours</button>
            <button className="reportsBtn" onClick={handleSelect48Hours}>Select All From Last 48 Hours</button>
            <button className="reportsBtn" onClick={handleSelectLast7Days}>Select All From Last 7 Days</button>
            <button className="reportsBtn" onClick={handleSelectNone}>Select None</button>
          </div>
        </div>
        <div className="main-box2">
          {Object.entries(rows.reduce((acc, row) => {
            const agencyId = row.agencyid;
            if (acc[agencyId]) {
              acc[agencyId].push(row);
            } else {
              acc[agencyId] = [row];
            }
            return acc;
          }, {})).map(([agencyId, rows]) => (
            <React.Fragment key={agencyId}>
              <h4>{agencyId}</h4>
              <table>
                <thead>
                  <tr>
                    <th>Select</th>
                    <th>Date and Time</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>Priority</th>
                    <th>Address</th>
                    <th>City</th>
                    <th>State</th>
                    <th>Zip Code</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.
                  sort((a, b) =>
                  sortOrder === "asc"
                    ? a.priority - b.priority
                    : b.priority - a.priority
                    )
                  .map((row) => (
                    <tr key={row.cid} onClick={() => handleRowClick(row.cid)}>
                      <td>
                        <input
                          type="checkbox"
                          checked={row.selected}
                          onChange={() => { }}
                        />
                      </td>
                      <td>{row.reported_dt}</td>
                      <td>{row.category}</td>
                      <td>{row.case_description}</td>
                      <td>{row.priority}</td>
                      <td>{row.addressline1}</td>
                      <td>{row.city}</td>
                      <td>{row.state}</td>
                      <td>{row.zipcode}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </React.Fragment>
          ))}
        </div>

        <div className="main-box3" >
          <button className="ignorebutton" onClick={handleIgnore}>Ignore</button>      
          <button className="publishbutton" onClick={handlePublish}>Publish</button>    
        {isVisible && <Banner message={message} isVisible={isVisible} isSuccess = {isSuccess} onClose={handleBannerClose}></Banner>}
        </div>

      </div>
    </div>
  );
}

export default PublishNewReports;

