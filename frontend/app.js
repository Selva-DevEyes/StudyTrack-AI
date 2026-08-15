/**
 * StudyTrack AI — Frontend JavaScript
 * Handles Roster CRUD, Event Delegation, Handwritten Algorithm & AI endpoints
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const studentForm = document.getElementById('student-form');
    const studentNameInput = document.getElementById('student-name');
    const studentEmailInput = document.getElementById('student-email');
    const studentAgeInput = document.getElementById('student-age');
    const rosterList = document.getElementById('roster-list');
    const rosterCountBadge = document.getElementById('roster-count-badge');
    
    // Controls & Algorithm Elements
    const sortBySelect = document.getElementById('sort-by-select');
    const binarySearchInput = document.getElementById('binary-search-input');
    const searchStudentBtn = document.getElementById('search-student-btn');
    const minAgeReportInput = document.getElementById('min-age-report-input');
    const generateReportBtn = document.getElementById('generate-report-btn');
    const reportOutput = document.getElementById('report-output');

    // Error Banner Elements
    const errorBanner = document.getElementById('error-banner');
    const errorMessageSpan = document.getElementById('error-message');
    const closeErrorBtn = document.getElementById('close-error-btn');

    // AI Helper Elements
    const aiNoteText = document.getElementById('ai-note-text');
    const summarizeBtn = document.getElementById('summarize-btn');
    const summaryResultBox = document.getElementById('summary-result');
    const summaryTopic = document.getElementById('summary-topic');
    const summaryDifficulty = document.getElementById('summary-difficulty');
    const summaryKeypoints = document.getElementById('summary-keypoints');
    const aiSearchQuery = document.getElementById('ai-search-query');
    const aiSearchBtn = document.getElementById('ai-search-btn');
    const aiSearchResultsContainer = document.getElementById('ai-search-results');
    const rankedNotesList = document.getElementById('ranked-notes-list');

    // --- State ---
    let currentStudents = [];

    // Base API URL (relative paths for single-process mode)
    const API_BASE = '';

    // --- Helper Functions ---

    function showError(msg) {
        if (!errorBanner || !errorMessageSpan) return;
        errorMessageSpan.textContent = msg;
        errorBanner.classList.remove('hidden');
    }

    function clearError() {
        if (!errorBanner) return;
        errorBanner.classList.add('hidden');
        if (errorMessageSpan) errorMessageSpan.textContent = '';
    }

    if (closeErrorBtn) {
        closeErrorBtn.addEventListener('click', clearError);
    }

    function updateRosterBadge(count) {
        if (rosterCountBadge) {
            rosterCountBadge.textContent = `${count} Student${count === 1 ? '' : 's'}`;
        }
    }

    /**
     * Constructs a student card element strictly using document.createElement()
     */
    function createStudentCardElement(student) {
        const card = document.createElement('div');
        card.className = 'student-card';
        card.setAttribute('data-id', student.id);

        // Header section (Name & Age display)
        const header = document.createElement('div');
        header.className = 'student-card-header';

        const nameEl = document.createElement('div');
        nameEl.className = 'student-name';
        nameEl.textContent = student.name;

        const ageBadge = document.createElement('span');
        ageBadge.className = 'student-age-badge';
        ageBadge.textContent = `Age: ${student.age}`;

        header.appendChild(nameEl);
        header.appendChild(ageBadge);

        // Email element
        const emailEl = document.createElement('div');
        emailEl.className = 'student-email';
        emailEl.textContent = student.email;

        // Actions section (Number input, Save Age, Delete)
        const actions = document.createElement('div');
        actions.className = 'student-card-actions';

        const ageInput = document.createElement('input');
        ageInput.type = 'number';
        ageInput.className = 'age-input';
        ageInput.min = '1';
        ageInput.value = student.age;
        ageInput.setAttribute('aria-label', `New age for ${student.name}`);

        const saveBtn = document.createElement('button');
        saveBtn.type = 'button';
        saveBtn.className = 'btn btn-save';
        saveBtn.textContent = 'Save Age';
        saveBtn.setAttribute('data-action', 'save-age');
        saveBtn.setAttribute('data-id', student.id);

        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'btn btn-delete';
        deleteBtn.textContent = 'Delete';
        deleteBtn.setAttribute('data-action', 'delete');
        deleteBtn.setAttribute('data-id', student.id);

        actions.appendChild(ageInput);
        actions.appendChild(saveBtn);
        actions.appendChild(deleteBtn);

        // Assemble card
        card.appendChild(header);
        card.appendChild(emailEl);
        card.appendChild(actions);

        return card;
    }

    /**
     * Render entire student roster list into DOM
     */
    function renderRoster(students) {
        currentStudents = students;
        rosterList.innerHTML = '';
        if (students.length === 0) {
            const emptyMsg = document.createElement('p');
            emptyMsg.className = 'text-muted';
            emptyMsg.style.padding = '20px';
            emptyMsg.textContent = 'No students found in the roster.';
            rosterList.appendChild(emptyMsg);
        } else {
            students.forEach(student => {
                const cardEl = createStudentCardElement(student);
                rosterList.appendChild(cardEl);
            });
        }
        updateRosterBadge(students.length);
    }

    // --- API Calls & Handlers ---

    /**
     * Fetch all students from backend GET /students/
     */
    async function loadRoster() {
        clearError();
        try {
            const res = await fetch(`${API_BASE}/students/`);
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || `Failed to fetch students (Status ${res.status})`);
            }
            const students = await res.json();
            renderRoster(students);
        } catch (err) {
            showError(err.message);
        }
    }

    /**
     * Add student handler (POST /students/)
     */
    if (studentForm) {
        studentForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent full page reload
            clearError();

            const name = studentNameInput.value.trim();
            const email = studentEmailInput.value.trim();
            const age = parseInt(studentAgeInput.value, 10);

            if (!name || !email || isNaN(age)) {
                showError('Please fill in all fields correctly.');
                return;
            }

            try {
                const res = await fetch(`${API_BASE}/students/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, age })
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || `Failed to add student (Status ${res.status})`);
                }

                // Append new student to state and DOM
                currentStudents.push(data);
                const cardEl = createStudentCardElement(data);
                
                // Remove empty message if present
                if (rosterList.children.length === 1 && rosterList.children[0].tagName === 'P') {
                    rosterList.innerHTML = '';
                }

                rosterList.appendChild(cardEl);
                updateRosterBadge(currentStudents.length);

                // Reset form inputs
                studentForm.reset();
            } catch (err) {
                showError(err.message);
            }
        });
    }

    /**
     * EVENT DELEGATION on #roster-list for Save Age and Delete
     */
    if (rosterList) {
        rosterList.addEventListener('click', async (e) => {
            const targetBtn = e.target.closest('button[data-action]');
            if (!targetBtn) return;

            const action = targetBtn.getAttribute('data-action');
            const studentId = parseInt(targetBtn.getAttribute('data-id'), 10);
            const cardEl = targetBtn.closest('.student-card');

            if (!studentId || !cardEl) return;
            clearError();

            if (action === 'save-age') {
                const ageInput = cardEl.querySelector('.age-input');
                const newAge = parseInt(ageInput.value, 10);

                if (isNaN(newAge) || newAge <= 0) {
                    showError('Age must be a positive integer.');
                    return;
                }

                try {
                    const res = await fetch(`${API_BASE}/students/${studentId}`, {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ age: newAge })
                    });

                    const data = await res.json();
                    if (!res.ok) {
                        throw new Error(data.detail || `Failed to update age (Status ${res.status})`);
                    }

                    // Update UI age display
                    const ageBadge = cardEl.querySelector('.student-age-badge');
                    if (ageBadge) {
                        ageBadge.textContent = `Age: ${data.age}`;
                    }

                    // Update local state
                    const idx = currentStudents.findIndex(s => s.id === studentId);
                    if (idx !== -1) currentStudents[idx].age = data.age;

                } catch (err) {
                    showError(err.message);
                }

            } else if (action === 'delete') {
                try {
                    const res = await fetch(`${API_BASE}/students/${studentId}`, {
                        method: 'DELETE'
                    });

                    if (!res.ok) {
                        const data = await res.json().catch(() => ({}));
                        throw new Error(data.detail || `Failed to delete student (Status ${res.status})`);
                    }

                    // Remove card from DOM
                    cardEl.remove();

                    // Update local state
                    currentStudents = currentStudents.filter(s => s.id !== studentId);
                    updateRosterBadge(currentStudents.length);

                    if (currentStudents.length === 0) {
                        renderRoster([]);
                    }

                } catch (err) {
                    showError(err.message);
                }
            }
        });
    }

    // --- Algorithm Endpoints Integration (Part 2) ---

    // 1. Insertion Sort Dropdown Handler
    if (sortBySelect) {
        sortBySelect.addEventListener('change', async () => {
            const field = sortBySelect.value;
            if (field === 'default') {
                loadRoster();
                return;
            }
            clearError();
            try {
                const res = await fetch(`${API_BASE}/students/sorted?by=${encodeURIComponent(field)}`);
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.detail || 'Failed to sort roster');
                }
                const sortedStudents = await res.json();
                renderRoster(sortedStudents);
            } catch (err) {
                showError(err.message);
            }
        });
    }

    // 2. Binary Search Button Handler
    if (searchStudentBtn && binarySearchInput) {
        searchStudentBtn.addEventListener('click', async () => {
            const queryName = binarySearchInput.value.trim();
            if (!queryName) {
                showError('Please enter a student name to search.');
                return;
            }
            clearError();
            try {
                const res = await fetch(`${API_BASE}/students/search?name=${encodeURIComponent(queryName)}`);
                if (!res.ok) {
                    if (res.status === 404) {
                        throw new Error(`Student "${queryName}" not found in roster.`);
                    }
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.detail || 'Binary search failed.');
                }
                const student = await res.json();
                // Highlight found student in roster
                renderRoster([student]);
                showError(`Found student: ${student.name} (Age ${student.age}, ${student.email})`);
            } catch (err) {
                showError(err.message);
            }
        });
    }

    // 3. Roster Report Button Handler
    if (generateReportBtn && minAgeReportInput && reportOutput) {
        generateReportBtn.addEventListener('click', async () => {
            const minAge = parseInt(minAgeReportInput.value, 10);
            if (isNaN(minAge)) {
                showError('Please enter a valid minimum age integer.');
                return;
            }
            clearError();
            try {
                const res = await fetch(`${API_BASE}/students/report?min_age=${minAge}`);
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.detail || 'Failed to generate report.');
                }
                const reportData = await res.json();
                reportOutput.textContent = reportData.report;
                reportOutput.classList.remove('hidden');
            } catch (err) {
                showError(err.message);
            }
        });
    }

    // --- AI Assistant Integration (Part 3) ---

    // 1. Note Summarizer Handler
    if (summarizeBtn && aiNoteText) {
        summarizeBtn.addEventListener('click', async () => {
            const text = aiNoteText.value;
            clearError();
            try {
                const res = await fetch(`${API_BASE}/assistant/summarize`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });

                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.detail || 'Failed to summarize notes.');
                }

                const summary = await res.json();

                // Populate Summary Result Box
                if (summaryTopic) summaryTopic.textContent = summary.topic;
                if (summaryDifficulty) {
                    summaryDifficulty.textContent = summary.difficulty;
                    summaryDifficulty.className = `badge difficulty-badge ${summary.difficulty}`;
                }

                if (summaryKeypoints) {
                    summaryKeypoints.innerHTML = '';
                    if (summary.key_points.length === 0) {
                        const li = document.createElement('li');
                        li.textContent = 'No key points extracted.';
                        summaryKeypoints.appendChild(li);
                    } else {
                        summary.key_points.forEach(point => {
                            const li = document.createElement('li');
                            li.textContent = point;
                            summaryKeypoints.appendChild(li);
                        });
                    }
                }

                if (summaryResultBox) summaryResultBox.classList.remove('hidden');

            } catch (err) {
                showError(err.message);
            }
        });
    }

    // 2. Semantic Search Handler
    if (aiSearchBtn && aiSearchQuery) {
        aiSearchBtn.addEventListener('click', async () => {
            const query = aiSearchQuery.value.trim();
            clearError();
            try {
                const res = await fetch(`${API_BASE}/assistant/search?query=${encodeURIComponent(query)}`);
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.detail || 'Semantic search failed.');
                }

                const rankedResults = await res.json();

                if (rankedNotesList) {
                    rankedNotesList.innerHTML = '';
                    rankedResults.forEach(item => {
                        const noteCard = document.createElement('div');
                        noteCard.className = 'ranked-note-item';

                        const scoreRow = document.createElement('div');
                        scoreRow.className = 'note-score-row';

                        const labelSpan = document.createElement('span');
                        labelSpan.className = 'note-id-label';
                        labelSpan.textContent = `Note ID: ${item.note_id}`;

                        const scorePill = document.createElement('span');
                        scorePill.className = 'score-pill';
                        scorePill.textContent = `Score: ${item.score.toFixed(4)}`;

                        scoreRow.appendChild(labelSpan);
                        scoreRow.appendChild(scorePill);

                        const textP = document.createElement('p');
                        textP.className = 'note-text';
                        textP.textContent = item.text;

                        noteCard.appendChild(scoreRow);
                        noteCard.appendChild(textP);

                        rankedNotesList.appendChild(noteCard);
                    });
                }

                if (aiSearchResultsContainer) aiSearchResultsContainer.classList.remove('hidden');

            } catch (err) {
                showError(err.message);
            }
        });
    }

    // Initialize Page
    loadRoster();
});
