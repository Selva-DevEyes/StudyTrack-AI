/**
 * StudyTrack AI — Frontend JavaScript Module
 * Features: Dark/Light Theme Switching, Roster CRUD, Course Management,
 * Stats Counter, Event Delegation, Handwritten Algorithms & AI Integration.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');

    const statTotalStudents = document.getElementById('stat-total-students');
    const statAvgAge = document.getElementById('stat-avg-age');
    const statTotalCourses = document.getElementById('stat-total-courses');

    const studentForm = document.getElementById('student-form');
    const studentNameInput = document.getElementById('student-name');
    const studentEmailInput = document.getElementById('student-email');
    const studentAgeInput = document.getElementById('student-age');
    
    const rosterList = document.getElementById('roster-list');
    const rosterCountBadge = document.getElementById('roster-count-badge');
    const rosterFilterInput = document.getElementById('roster-filter-input');
    
    const sortBySelect = document.getElementById('sort-by-select');
    const binarySearchInput = document.getElementById('binary-search-input');
    const searchStudentBtn = document.getElementById('search-student-btn');
    const minAgeReportInput = document.getElementById('min-age-report-input');
    const generateReportBtn = document.getElementById('generate-report-btn');
    const reportOutput = document.getElementById('report-output');

    const errorBanner = document.getElementById('error-banner');
    const errorMessageSpan = document.getElementById('error-message');
    const closeErrorBtn = document.getElementById('close-error-btn');

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
    const API_BASE = '';

    // --- Theme Switcher Logic ---
    function initTheme() {
        const savedTheme = localStorage.getItem('studytrack-theme') || 'dark';
        setTheme(savedTheme);
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('studytrack-theme', theme);
        if (theme === 'light') {
            if (themeIcon) themeIcon.textContent = '🌙';
            if (themeText) themeText.textContent = 'Dark Mode';
        } else {
            if (themeIcon) themeIcon.textContent = '☀️';
            if (themeText) themeText.textContent = 'Light Mode';
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }

    initTheme();

    // --- Error Banner Helpers ---
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

    // --- Stats Bar Calculator ---
    function updateStats(students) {
        const total = students.length;
        if (statTotalStudents) statTotalStudents.textContent = total;

        if (total === 0) {
            if (statAvgAge) statAvgAge.textContent = '0';
            if (statTotalCourses) statTotalCourses.textContent = '0';
            return;
        }

        const sumAge = students.reduce((acc, s) => acc + s.age, 0);
        const avg = (sumAge / total).toFixed(1);
        if (statAvgAge) statAvgAge.textContent = avg;

        let totalCourses = 0;
        students.forEach(s => {
            if (s.courses && Array.isArray(s.courses)) {
                totalCourses += s.courses.length;
            }
        });
        if (statTotalCourses) statTotalCourses.textContent = totalCourses;
    }

    function updateRosterBadge(count) {
        if (rosterCountBadge) {
            rosterCountBadge.textContent = `${count} Trainee${count === 1 ? '' : 's'}`;
        }
    }

    // --- Dynamic Card Creation via document.createElement() ---
    function createStudentCardElement(student) {
        const card = document.createElement('div');
        card.className = 'student-card';
        card.setAttribute('data-id', student.id);

        // Header Section
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

        // Email Section
        const emailEl = document.createElement('div');
        emailEl.className = 'student-email';
        emailEl.textContent = student.email;

        // Enrolled Courses Section
        const coursesSec = document.createElement('div');
        coursesSec.className = 'student-courses-section';

        const coursesHeader = document.createElement('div');
        coursesHeader.className = 'courses-header';

        const coursesTitle = document.createElement('span');
        coursesTitle.className = 'courses-title';
        const courseCount = student.courses ? student.courses.length : 0;
        coursesTitle.textContent = `Enrolled Courses (${courseCount})`;
        coursesHeader.appendChild(coursesTitle);

        const coursesList = document.createElement('div');
        coursesList.className = 'courses-list';

        if (student.courses && student.courses.length > 0) {
            student.courses.forEach(c => {
                const chip = document.createElement('span');
                chip.className = 'course-chip';
                chip.innerHTML = `${c.course_name} <span class="course-chip-delete" data-action="delete-course" data-course-id="${c.id}" data-student-id="${student.id}" title="Remove course">&times;</span>`;
                coursesList.appendChild(chip);
            });
        } else {
            const noCourses = document.createElement('span');
            noCourses.className = 'text-muted';
            noCourses.style.fontSize = '0.75rem';
            noCourses.textContent = 'No enrolled courses';
            coursesList.appendChild(noCourses);
        }

        // Simplified Add Course Form (No confusing credit select for beginners)
        const addCourseForm = document.createElement('div');
        addCourseForm.className = 'add-course-form';

        const courseInput = document.createElement('input');
        courseInput.type = 'text';
        courseInput.placeholder = 'Add Course (e.g. Python)...';
        courseInput.className = 'course-name-input';

        const addCourseBtn = document.createElement('button');
        addCourseBtn.type = 'button';
        addCourseBtn.className = 'btn btn-secondary btn-sm';
        addCourseBtn.textContent = '+ Add';
        addCourseBtn.setAttribute('data-action', 'add-course');
        addCourseBtn.setAttribute('data-id', student.id);

        addCourseForm.appendChild(courseInput);
        addCourseForm.appendChild(addCourseBtn);

        coursesSec.appendChild(coursesHeader);
        coursesSec.appendChild(coursesList);
        coursesSec.appendChild(addCourseForm);

        // Actions Section (Age update & Delete student)
        const actions = document.createElement('div');
        actions.className = 'student-card-actions';

        const ageInput = document.createElement('input');
        ageInput.type = 'number';
        ageInput.className = 'age-input';
        ageInput.min = '1';
        ageInput.value = student.age;

        const saveBtn = document.createElement('button');
        saveBtn.type = 'button';
        saveBtn.className = 'btn btn-save btn-cta';
        saveBtn.textContent = 'Save Age';
        saveBtn.setAttribute('data-action', 'save-age');
        saveBtn.setAttribute('data-id', student.id);

        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'btn btn-delete btn-cta';
        deleteBtn.textContent = 'Delete';
        deleteBtn.setAttribute('data-action', 'delete');
        deleteBtn.setAttribute('data-id', student.id);

        actions.appendChild(ageInput);
        actions.appendChild(saveBtn);
        actions.appendChild(deleteBtn);

        // Assemble card
        card.appendChild(header);
        card.appendChild(emailEl);
        card.appendChild(coursesSec);
        card.appendChild(actions);

        return card;
    }

    function renderRoster(students) {
        currentStudents = students;
        updateStats(students);

        const filterQuery = rosterFilterInput ? rosterFilterInput.value.trim().toLowerCase() : '';
        const filtered = filterQuery 
            ? students.filter(s => s.name.toLowerCase().includes(filterQuery) || s.email.toLowerCase().includes(filterQuery))
            : students;

        rosterList.innerHTML = '';
        if (filtered.length === 0) {
            const emptyMsg = document.createElement('p');
            emptyMsg.className = 'text-muted';
            emptyMsg.style.padding = '20px';
            emptyMsg.textContent = filterQuery ? 'No matching trainees found.' : 'No trainees found in the roster.';
            rosterList.appendChild(emptyMsg);
        } else {
            filtered.forEach(student => {
                const cardEl = createStudentCardElement(student);
                rosterList.appendChild(cardEl);
            });
        }
        updateRosterBadge(filtered.length);
    }

    if (rosterFilterInput) {
        rosterFilterInput.addEventListener('input', () => {
            renderRoster(currentStudents);
        });
    }

    // --- API Calls ---
    async function loadRoster() {
        clearError();
        try {
            const res = await fetch(`${API_BASE}/students/`);
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.detail || `Failed to fetch roster (Status ${res.status})`);
            }
            const students = await res.json();
            renderRoster(students);
        } catch (err) {
            showError(err.message);
        }
    }

    // --- Student Form Handler ---
    if (studentForm) {
        studentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearError();

            const name = studentNameInput.value.trim();
            const email = studentEmailInput.value.trim();
            const age = parseInt(studentAgeInput.value, 10);

            if (!name || !email || isNaN(age)) {
                showError('Please fill in all required student fields.');
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

                currentStudents.push(data);
                renderRoster(currentStudents);
                studentForm.reset();
            } catch (err) {
                showError(err.message);
            }
        });
    }

    // --- Event Delegation on #roster-list ---
    if (rosterList) {
        rosterList.addEventListener('click', async (e) => {
            // 1. Delete Course Action
            const deleteCourseBtn = e.target.closest('[data-action="delete-course"]');
            if (deleteCourseBtn) {
                const courseId = parseInt(deleteCourseBtn.getAttribute('data-course-id'), 10);
                const studentId = parseInt(deleteCourseBtn.getAttribute('data-student-id'), 10);
                clearError();
                try {
                    const res = await fetch(`${API_BASE}/courses/${courseId}`, { method: 'DELETE' });
                    if (!res.ok) {
                        const errData = await res.json().catch(() => ({}));
                        throw new Error(errData.detail || 'Failed to delete course');
                    }
                    loadRoster(); // Reload to refresh course lists
                } catch (err) {
                    showError(err.message);
                }
                return;
            }

            // 2. Add Course Action
            const addCourseBtn = e.target.closest('[data-action="add-course"]');
            if (addCourseBtn) {
                const studentId = parseInt(addCourseBtn.getAttribute('data-id'), 10);
                const cardEl = addCourseBtn.closest('.student-card');
                const nameInput = cardEl.querySelector('.course-name-input');
                const courseName = nameInput.value.trim();
                const credits = 3; // Default 3 credits for academic course

                if (!courseName) {
                    showError('Please enter a course name.');
                    return;
                }

                clearError();
                try {
                    const res = await fetch(`${API_BASE}/courses/`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ course_name: courseName, credits, student_id: studentId })
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        throw new Error(data.detail || 'Failed to add course');
                    }
                    loadRoster(); // Reload roster to reflect new course
                } catch (err) {
                    showError(err.message);
                }
                return;
            }

            // 3. Save Age Action
            const saveAgeBtn = e.target.closest('[data-action="save-age"]');
            if (saveAgeBtn) {
                const studentId = parseInt(saveAgeBtn.getAttribute('data-id'), 10);
                const cardEl = saveAgeBtn.closest('.student-card');
                const ageInput = cardEl.querySelector('.age-input');
                const newAge = parseInt(ageInput.value, 10);

                if (isNaN(newAge) || newAge <= 0) {
                    showError('Age must be a positive integer.');
                    return;
                }

                clearError();
                try {
                    const res = await fetch(`${API_BASE}/students/${studentId}`, {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ age: newAge })
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        throw new Error(data.detail || 'Failed to update age');
                    }

                    const ageBadge = cardEl.querySelector('.student-age-badge');
                    if (ageBadge) ageBadge.textContent = `Age: ${data.age}`;

                    const idx = currentStudents.findIndex(s => s.id === studentId);
                    if (idx !== -1) currentStudents[idx].age = data.age;
                    updateStats(currentStudents);
                } catch (err) {
                    showError(err.message);
                }
                return;
            }

            // 4. Delete Student Action
            const deleteStudentBtn = e.target.closest('[data-action="delete"]');
            if (deleteStudentBtn) {
                const studentId = parseInt(deleteStudentBtn.getAttribute('data-id'), 10);
                const cardEl = deleteStudentBtn.closest('.student-card');

                clearError();
                try {
                    const res = await fetch(`${API_BASE}/students/${studentId}`, { method: 'DELETE' });
                    if (!res.ok) {
                        const data = await res.json().catch(() => ({}));
                        throw new Error(data.detail || 'Failed to delete student');
                    }

                    cardEl.remove();
                    currentStudents = currentStudents.filter(s => s.id !== studentId);
                    renderRoster(currentStudents);
                } catch (err) {
                    showError(err.message);
                }
                return;
            }
        });
    }

    // --- Handwritten Algorithms Integration ---
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
                renderRoster([student]);
                showError(`Found student: ${student.name} (Age ${student.age}, ${student.email})`);
            } catch (err) {
                showError(err.message);
            }
        });
    }

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

    // --- AI Assistant Integration ---
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
                        labelSpan.textContent = `Note ID: ${item.id || item.note_id}`;

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

    // Initial Load
    loadRoster();
});
