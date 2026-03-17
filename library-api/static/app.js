const API_BASE = "/api/books";

const form = document.getElementById("book-form");
const booksList = document.getElementById("books-list");
const emptyState = document.getElementById("empty-state");
const formTitle = document.getElementById("form-title");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");
const bookIdInput = document.getElementById("book-id");

// Fetch and display all books
async function loadBooks() {
  try {
    const res = await fetch(API_BASE);
    const books = await res.json();
    renderBooks(books);
  } catch (err) {
    emptyState.textContent = "Failed to load books. Is the server running?";
    emptyState.classList.add("error");
  }
}

function renderBooks(books) {
  if (books.length === 0) {
    emptyState.textContent = "No books yet. Add one above!";
    emptyState.style.display = "block";
    booksList.innerHTML = "";
    return;
  }

  emptyState.style.display = "none";
  booksList.innerHTML = books
    .map(
      (book) => `
    <div class="book-card" data-id="${book.id}">
      <div class="book-info">
        <h3>${escapeHtml(book.title)}</h3>
        <p>${escapeHtml(book.author)} · ${escapeHtml(book.genre)} (${book.year_published})</p>
        <span class="badge ${book.is_available ? "available" : "unavailable"}">
          ${book.is_available ? "Available" : "Checked out"}
        </span>
      </div>
      <div class="book-actions">
        <button class="btn-edit" onclick="editBook(${book.id})">Edit</button>
        <button class="btn-delete" onclick="deleteBook(${book.id})">Delete</button>
      </div>
    </div>
  `
    )
    .join("");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Form submit - create or update
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = bookIdInput.value;
  const payload = {
    title: document.getElementById("title").value.trim(),
    author: document.getElementById("author").value.trim(),
    genre: document.getElementById("genre").value.trim(),
    year_published: parseInt(document.getElementById("year").value, 10),
    is_available: document.getElementById("available").checked,
  };

  try {
    if (id) {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("Update failed");
    } else {
      const res = await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("Create failed");
    }
    resetForm();
    loadBooks();
  } catch (err) {
    alert("Something went wrong. Check the console.");
    console.error(err);
  }
});

cancelBtn.addEventListener("click", resetForm);

function resetForm() {
  bookIdInput.value = "";
  form.reset();
  document.getElementById("available").checked = true;
  formTitle.textContent = "Add New Book";
  submitBtn.textContent = "Add Book";
  cancelBtn.style.display = "none";
}

async function editBook(id) {
  const res = await fetch(`${API_BASE}/${id}`);
  const book = await res.json();
  document.getElementById("book-id").value = book.id;
  document.getElementById("title").value = book.title;
  document.getElementById("author").value = book.author;
  document.getElementById("genre").value = book.genre;
  document.getElementById("year").value = book.year_published;
  document.getElementById("available").checked = book.is_available;
  formTitle.textContent = "Edit Book";
  submitBtn.textContent = "Save Changes";
  cancelBtn.style.display = "inline-block";
}

async function deleteBook(id) {
  if (!confirm("Delete this book?")) return;
  try {
    const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Delete failed");
    loadBooks();
  } catch (err) {
    alert("Failed to delete.");
    console.error(err);
  }
}

loadBooks();
