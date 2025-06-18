# Instructor API Endpoints

This document describes the instructor-specific API endpoints that allow instructors to manage their courses and access instructor-specific functionality.

## Authentication

All instructor endpoints require authentication using a Bearer token. The token must be obtained by logging in as an instructor user through the `/api/v1/auth/login` endpoint.

## Base URL

All instructor endpoints are prefixed with `/api/v1/instructor`

## Endpoints

### Profile Management

#### GET `/api/v1/instructor/profile`
Get the current instructor's profile information.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "username": "instructor1",
  "email": "instructor@example.com",
  "user_type": "instructor"
}
```

#### GET `/api/v1/instructor/dashboard`
Get instructor dashboard statistics including course count and enrollment statistics.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
{
  "instructor_id": 1,
  "total_courses": 5,
  "total_enrollments": 25,
  "message": "Instructor dashboard data retrieved successfully"
}
```

### Course Management

#### POST `/api/v1/instructor/courses/create`
Create a new course. Only instructors can create courses.

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Introduction to Python Programming",
  "description": "Learn the basics of Python programming language"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Introduction to Python Programming",
  "description": "Learn the basics of Python programming language",
  "instructor_id": 1
}
```

#### GET `/api/v1/instructor/courses/my-courses`
Get all courses created by the current instructor.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Introduction to Python Programming",
    "description": "Learn the basics of Python programming language",
    "instructor_id": 1
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "Advanced Python",
    "description": "Advanced Python concepts and techniques",
    "instructor_id": 1
  }
]
```

#### GET `/api/v1/instructor/courses/course/{course_id}`
Get a specific course by ID. Only the instructor who created the course can access it.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Introduction to Python Programming",
  "description": "Learn the basics of Python programming language",
  "instructor_id": 1
}
```

#### PUT `/api/v1/instructor/courses/course/{course_id}`
Update a course. Only the instructor who created the course can update it.

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body:**
```json
{
  "title": "Updated Course Title",
  "description": "Updated course description"
}
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Course Title",
  "description": "Updated course description",
  "instructor_id": 1
}
```

#### DELETE `/api/v1/instructor/courses/course/{course_id}`
Delete a course. Only the instructor who created the course can delete it.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
{
  "message": "Course deleted successfully"
}
```

#### GET `/api/v1/instructor/courses/all-courses`
Get all courses in the system. This endpoint is accessible to instructors to view all available courses.

**Headers:**
- `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Introduction to Python Programming",
    "description": "Learn the basics of Python programming language",
    "instructor_id": 1
  }
]
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied. Only instructors can perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Course not found or you don't have permission to access it"
}
```

## Security Features

1. **Role-based Access Control**: Only users with `user_type: "instructor"` can access these endpoints
2. **Ownership Validation**: Instructors can only manage courses they created
3. **Token-based Authentication**: All endpoints require valid JWT tokens
4. **Automatic Instructor ID Assignment**: Course creation automatically assigns the instructor ID from the authenticated user

## Usage Examples

### Creating a Course
```bash
curl -X POST "http://localhost:8000/api/v1/instructor/courses/create" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Web Development Fundamentals",
    "description": "Learn HTML, CSS, and JavaScript basics"
  }'
```

### Getting My Courses
```bash
curl -X GET "http://localhost:8000/api/v1/instructor/courses/my-courses" \
  -H "Authorization: Bearer <your_token>"
```

### Updating a Course
```bash
curl -X PUT "http://localhost:8000/api/v1/instructor/courses/course/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Web Development Course",
    "description": "Comprehensive web development course with modern frameworks"
  }'
``` 