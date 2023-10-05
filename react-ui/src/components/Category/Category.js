
import React, { useState, useEffect } from "react";
import "./Category.css";

function Category(props) {
  var session_token = localStorage.getItem('session_token');
  const [categories, setCategories] = useState([]);
  const [categoriesByPriority, setCategoriesByPriority] = useState([]);
  const [newCategory, setNewCategory] = useState("");
  const [editedPriority, setEditedPriority] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hoveredRow, setHoveredRow] = useState(null);
  const baseuri = process.env.REACT_APP_BACKEND_SERVER_URL;


  useEffect(() => {
    fetchCategories();
    fetchCategoriesByPriority();
  }, []);

  function fetchCategories() {
    fetch(baseuri + "/categories", {
      method: "GET",
      headers: {
        "session-token": session_token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.response);
        data = data.response;
        setCategories(data);
      })
      .catch((error) => console.error("Error fetching categories:", error));
  }

  function fetchCategoriesByPriority() {
    var pubId = localStorage.getItem('selected_publication')
    fetch(baseuri + "/category_priority_list" + "?pubId=" + pubId, {
      method: "GET",
      headers: {
        "session-token": session_token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.response);
        data = data.response;
        setCategoriesByPriority(data);
      })
      .catch((error) => console.error("Error fetching categories by priority:", error));
  }


  function handleSortCategories() {
    const sortedCategories = [...categories].sort((a, b) =>
      a.category_name.localeCompare(b.category_name)
    );
    setCategories(sortedCategories);
  }

  function handleNewCategoryInputChange(event) {
    setNewCategory(event.target.value);
  }

  function handleAddCategory() {
    if (newCategory.trim() === "") {
      return;
    }
    setIsSubmitting(true);
    fetch(baseuri + "/categories?category_name=" + encodeURIComponent(newCategory), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "session-token": session_token,
      },
      body: JSON.stringify({
        user_id: props.user_id,
        category_name: newCategory,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.response);
        if (data.response !== "Category already exists") {
          setCategories([...categories, data.response]);
          setNewCategory("");
          fetchCategoriesByPriority()
        }
      })
      .catch((error) => console.error("Error adding category:", error))
      .finally(() => setIsSubmitting(false));
  }

  function deleteCategory(categoryId) {
    console.log(props.user_id)
    fetch(baseuri + `/categories?user_id=${props.user_id}&category_id=${categoryId}`, {
      method: "DELETE",
      headers: {
        "session-token": session_token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.response);
        if (data.response === "Deleted the category successfully") {
          // Filter out the deleted category from the categories list
          const updatedCategories = categories.filter(
            (category) => category.category_id !== categoryId
          );
          setCategories(updatedCategories);
          fetchCategoriesByPriority()
        }
      })
      .catch((error) => console.error("Error deleting category:", error));
  }

  const handleKeyDown = (e, categoryByPriority) => {
    if (e.key === 'Enter') {
      e.preventDefault(); 
      setEditedPriority(e.target.value);
      console.log("Pressed Enter")
      if (e.target.value === "") {
        return;
      }
      var pubId = localStorage.getItem('selected_publication')
      fetch(baseuri + "/category_priority_list?category_id=" + encodeURIComponent(categoryByPriority.category_id) + "&pub_id=" + pubId + "&priority=" + encodeURIComponent(e.target.value) , {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "session-token": session_token,
        },
        body: JSON.stringify({
          user_id: props.user_id,
          category_name: newCategory,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.response);
          if (data.response !== "Category already exists") {
            fetchCategoriesByPriority()
          }
        })
        .catch((error) => console.error("Error adding category:", error))
        .finally(() => setEditedPriority(""));
    }
  };

  function deletePriority(priorityId) {
    console.log(props.user_id)
    fetch(baseuri + `/category_priority_list?priority_id=${priorityId}`, {
      method: "DELETE",
      headers: {
        "session-token": session_token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.response);
        if (data.response === "Deleted the priority successfully") {
          // Filter out the deleted category from the categories list
          fetchCategoriesByPriority()
        }
      })
      .catch((error) => console.error("Error deleting category:", error));
  }
  
  

  return (
    <div className="category-container">
      <div className="category-box">
        <div className="category-box1">
          <h4 className="category-title">Category</h4>
        </div>
        <div className="category-box2">
          <table>
            <thead className="categories-table-header">
              <tr>
                <th onClick={handleSortCategories} className="category-header">
                  Category
                </th>
                {/* <th>Description</th> */}
              </tr>
            </thead>
            <tbody>
              {categories.map((category) => (
                <tr
                  key={category.category_id}
                  className={hoveredRow === category.category_id ? "hovered-row" : ""}
                  onMouseEnter={() => setHoveredRow(category.category_id)}
                  onMouseLeave={() => setHoveredRow(null)}
                >
                  <td>{category.category_name}</td>
                  <td>
                    {hoveredRow === category.category_id && (
                      <button
                        onClick={() => deleteCategory(category.category_id)}
                        className="delete-category-button"
                      >
                        x
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              <tr>
                <td>
                  <input
                    type="text"
                    value={newCategory}
                    onChange={handleNewCategoryInputChange}
                    placeholder="New Category"
                    className="new-category-input"
                  />
                </td>
                <td>
                  <button
                    onClick={handleAddCategory}
                    disabled={isSubmitting}
                    className="add-category-button"
                  >
                    {isSubmitting ? "Adding..." : "Add Category"}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div className="priority-box">
        <div className="category-box1">
          <h4 className="category-title">Priority</h4>
        </div>
        <div className="category-box2">
          <table>
            <thead className="categories-table-header">
              <tr>
                <th onClick={handleSortCategories} className="category-header">
                  Category
                </th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody>
              {categoriesByPriority.map((categoryByPriority) => (
                <tr
                  key={categoryByPriority.category_id}
                  className={hoveredRow === categoryByPriority.category_id ? "hovered-row" : ""}
                  onMouseEnter={() => setHoveredRow(categoryByPriority.category_id)}
                  onMouseLeave={() => setHoveredRow(null)}
                >
                  <td>{categoryByPriority.category_name}</td>
                  <td>
                    {hoveredRow === categoryByPriority.category_id ? (
                    <input
                        style={{ width: '50px', height: '10px' }}
                        type="text"
                        // value={editedPriority === categoryByPriority.priority ? categoryByPriority.priority : editedPriority }
                        value={categoryByPriority.priority }
                        onChange={(e) => setEditedPriority(e.target.value)}
                        onKeyDown={(e) => handleKeyDown(e, categoryByPriority)}
                    />
                    ) : (
                    categoryByPriority.priority
                    )}
                  </td>
                  <td>
                    {hoveredRow === categoryByPriority.category_id && (
                      <button
                        onClick={() => deletePriority(categoryByPriority.priority_id)}
                        className="delete-category-button"
                      >
                        x
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );  
}

export default Category;
