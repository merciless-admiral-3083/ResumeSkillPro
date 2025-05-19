import React, { useState, useEffect } from 'react';
import '../styles/SkillsList.css';

/**
 * Component to display extracted skills
 * @param {Object} props - Component props
 * @param {Object} props.skills - Object containing categorized skills
 */
const SkillsList = ({ skills }) => {
  const [expandedCategories, setExpandedCategories] = useState({});

  useEffect(() => {
    const categories = Object.keys(skills);
    if (categories.length > 0) {
      const initial = {};
      initial[categories[0]] = true;
      setExpandedCategories(initial);
    }
  }, [skills]);

  const getTotalSkillsCount = () => {
    return Object.values(skills).reduce((total, categorySkills) => total + categorySkills.length, 0);
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Programming Languages': 'primary',
      'Web Development': 'info',
      'Data Science': 'success',
      'Database': 'warning',
      'DevOps': 'danger',
      'Other': 'secondary',
      'Error': 'danger',
      'Notice': 'info'
    };
    
    return colors[category] || 'secondary';
  };

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  return (
    <div className="skills-container">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4>Found {getTotalSkillsCount()} skills in {Object.keys(skills).length} categories</h4>
      </div>
        
      <div className="accordion" id="skillsAccordion">
        {Object.entries(skills).map(([category, categorySkills], index) => (
          <div className="accordion-item" key={category}>
            <h2 className="accordion-header" id={`heading${index}`}>
              <button 
                className={`accordion-button ${!expandedCategories[category] ? 'collapsed' : ''}`} 
                type="button" 
                onClick={() => toggleCategory(category)}
              >
                <span className={`badge bg-${getCategoryColor(category)} me-2`}>
                  {categorySkills.length}
                </span>
                {category}
              </button>
            </h2>
            <div 
              className={`accordion-collapse ${expandedCategories[category] ? 'show' : 'collapse'}`}
            >
              <div className="accordion-body">
                <div className="skill-tags">
                  {categorySkills.map(skill => (
                    <span key={skill} className={`badge bg-${getCategoryColor(category)} skill-tag`}>
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-dark rounded border">
        <h5 className="mb-3">
          <i className="fas fa-lightbulb text-warning me-2"></i>
          Tips for your resume
        </h5>
        <ul className="list-group list-group-flush">
          <li className="list-group-item bg-transparent">Match skills to the job description you're applying for</li>
          <li className="list-group-item bg-transparent">Highlight your top skills in your summary section</li>
          <li className="list-group-item bg-transparent">Use specific examples of how you've applied these skills</li>
          <li className="list-group-item bg-transparent">Include both technical skills and soft skills for balance</li>
        </ul>
      </div>
    </div>
  );
};

export default SkillsList;