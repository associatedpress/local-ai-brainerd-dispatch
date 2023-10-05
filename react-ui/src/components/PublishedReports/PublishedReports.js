import React, { useState, useEffect } from "react";
import "./PublishedReports.css";

function PublishedReports(props) {
  //console.log('Session token:', props.session_token);
  var session_token = localStorage.getItem('session_token');
  const [selectedRows, setSelectedRows] = useState([]);
  const [rows, setRows] = useState([]);
  const [sortOrder, setSortOrder] = useState("asc");
  const [filters, setFilters] = useState([{"filter_id": 20, "filter_name" : "fetch recent 20 reports"}, {"filter_id": 40, "filter_name" : "fetch recent 40 reports"}, {"filter_id": 100, "filter_name" : "fetch recent 100 reports"}]);
  const [selectedFilter, setSelectedFilter] = useState("");
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;
  


  useEffect(() => {
    fetchReports();
  }, [selectedFilter]);

  function fetchReports ()
  {
    console.log()
    var uri;
    if (selectedFilter == null)
    {
      uri = baseuri + "/getpublishedreports"
    }
    else 
    {
      uri = baseuri + "/getpublishedreports?record_count=" + selectedFilter;
    }

    fetch(uri, {
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
      .catch(error => console.error('Error fetching published reports:', error));
  } 

  const handleRowClick = (id) => {
    setRows((prevRows) =>
      prevRows.map((row) => {
        if (row.cid === id) {
          return { ...row, selected: !row.selected };
        } else {
          return row;
        }
      })
    );
  };

  function handleFilterChange(event) {
    console.log("Filter changed")
    setSelectedFilter(event.target.value);
  }

  return (
    <div className="main-container">
      <div className="main-box">
        <div className="main-box1">
          <h4 className="blotterItems">Recently Published Reports</h4>
          <div className="filter-box1">
          <h4 className="filterTitle">
            Select the filter
          </h4>
          <select className="filterDropdown" value={selectedFilter} onChange={handleFilterChange}>
            <option value="">Select the filter</option>
            {filters.map((filter) => (
              <option key={filter.filter_id} value={filter.filter_id}>
                {filter.filter_name}
              </option>
            ))}
          </select>
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
                    <th>Date and Time</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}>Priority</th>
                    <th>Address</th>
                    <th>City</th>
                    <th>State</th>
                    <th>Zip Code</th>
                    <th>Publication</th>
                    <th>User</th>
                    <th>Report Sent Date</th>
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
                      <td>{row.reported_dt}</td>
                      <td>{row.category}</td>
                      <td>{row.case_description}</td>
                      <td>{row.priority}</td>
                      <td>{row.addressline1}</td>
                      <td>{row.city}</td>
                      <td>{row.state}</td>
                      <td>{row.zipcode}</td>
                      <td>{row.publication}</td>
                      <td>{row.user}</td>
                      <td>{row.report_sent_dt}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </React.Fragment>
          ))}
        </div>
        <div className="main-box3" ></div>

      </div>
    </div>
  );
}

export default PublishedReports;

