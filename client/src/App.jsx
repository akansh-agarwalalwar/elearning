import React from 'react';
import { Search, ChevronDown, ArrowRight } from 'lucide-react';

// Reusable Button Component
const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  onClick,
  ...props 
}) => {
  const baseClasses = 'font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
    secondary: 'bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 focus:ring-blue-500',
    ghost: 'hover:bg-gray-100 text-gray-700'
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };
  
  return (
    <button
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

// Reusable Card Component
const Card = ({ children, className = '', ...props }) => {
  return (
    <div 
      className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

// Progress Bar Component
const ProgressBar = ({ progress, className = '' }) => {
  return (
    <div className={`w-full bg-gray-200 rounded-full h-2 ${className}`}>
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
};

// Course Card Component
const CourseCard = ({ 
  title, 
  instructor, 
  progress, 
  image, 
  onContinue 
}) => {
  return (
    <Card className="hover:shadow-md transition-shadow duration-200">
      <div className="aspect-video bg-gray-100 relative overflow-hidden">
        <img 
          src={image} 
          alt={title}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-6">
        <h3 className="font-semibold text-gray-900 text-lg mb-2">{title}</h3>
        <p className="text-gray-600 text-sm mb-4">{instructor}</p>
        
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">Progress</span>
            <span className="text-sm font-medium text-gray-900">{progress}%</span>
          </div>
          <ProgressBar progress={progress} />
        </div>
        
        <Button 
          variant="primary" 
          className="w-full"
          onClick={onContinue}
        >
          Continue Learning
        </Button>
      </div>
    </Card>
  );
};

// Header Component
const Header = ({ user }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <div className="text-2xl font-bold text-blue-600">EduLearn</div>
          <nav className="hidden md:flex space-x-6">
            <a href="#" className="text-blue-600 font-medium border-b-2 border-blue-600 pb-2">
              Dashboard
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 pb-2">
              My Courses
            </a>
            <a href="#" className="text-gray-600 hover:text-gray-900 pb-2">
              Assignments
            </a>
          </nav>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search courses..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded-lg">
            <img
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face"
              alt={user.name}
              className="w-8 h-8 rounded-full"
            />
            <span className="text-gray-700 font-medium">{user.name}</span>
            <ChevronDown className="w-4 h-4 text-gray-500" />
          </div>
        </div>
      </div>
    </header>
  );
};

// Hero Section Component
const HeroSection = ({ user, onExplore }) => {
  return (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-12">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex-1">
          <h1 className="text-4xl font-bold mb-4">Welcome back, {user.name}!</h1>
          <p className="text-blue-100 text-lg mb-8 max-w-md">
            Continue your learning journey and explore new courses to enhance your skills.
          </p>
          <Button 
            variant="secondary" 
            size="lg"
            onClick={onExplore}
          >
            Explore Courses
          </Button>
        </div>
        
        <div className="hidden lg:block flex-shrink-0 ml-8">
          <img
            src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=300&fit=crop"
            alt="Learning"
            className="w-80 h-60 object-cover rounded-lg shadow-lg"
          />
        </div>
      </div>
    </div>
  );
};

// Main Dashboard Component
const App = () => {
  const user = {
    name: "John Doe"
  };
  
  const courses = [
    {
      id: 1,
      title: "Introduction to Web Development",
      instructor: "Prof. Sarah Johnson",
      progress: 65,
      image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400&h=225&fit=crop"
    },
    {
      id: 2,
      title: "Data Science Fundamentals",
      instructor: "Dr. Michael Chen",
      progress: 32,
      image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop"
    }
  ];
  
  const handleContinueCourse = (courseId) => {
    console.log(`Continuing course ${courseId}`);
  };
  
  const handleExploreCourses = () => {
    console.log("Exploring courses");
  };
  
  const handleViewAll = () => {
    console.log("Viewing all courses");
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} />
      
      <HeroSection user={user} onExplore={handleExploreCourses} />
      
      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Continue Learning</h2>
          <button 
            onClick={handleViewAll}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium"
          >
            <span>View All</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              title={course.title}
              instructor={course.instructor}
              progress={course.progress}
              image={course.image}
              onContinue={() => handleContinueCourse(course.id)}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default App;