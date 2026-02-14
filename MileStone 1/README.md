# FitPlan-AI-Personalized-Fitness-Plan-Generator
Objective of the Milestone
The objective of this milestone is to design and develop the initial version of the FitPlan AI web application that allows users to:
	Enter their basic physical details (Name, Height, Weight).
	Calculate their Body Mass Index (BMI).
	View their BMI category.
	Experience a visually attractive and user-friendly interface.
	Lay the foundation for future features like personalized workout and diet plans.
This milestone mainly focuses on UI design, input handling, BMI logic, and basic analytics visualization.
________________________________________
BMI Formula Explanation
BMI (Body Mass Index) is a simple calculation used to assess whether a person’s weight is appropriate for their height.
Formula
 BMI = weight (kg) / (height in meters)²
Example
	Height = 170 cm → 1.70 m
	Weight = 65 kg
BMI=65/(1.7×1.7)=22.49


Steps Performed in Milestone 1
1. Form Creation
•	Built a Streamlit web interface.
•	Added input fields:
o	Name
o	Height (cm)
o	Weight (kg)
o	Fitness Goal
o	Equipment
o	Fitness Level
•	Designed a sidebar for tips and BMI information.
•	Applied CSS styling and background images for attractive UI.
________________________________________
2. Input Validation
•	Ensured:
o	Name is not empty.
o	Height > 0
o	Weight > 0
•	Displayed error messages if invalid inputs are provided.
________________________________________
3. BMI Logic Implementation
•	Converted height from cm to meters.
•	Applied BMI formula.
•	Determined BMI category using conditional logic.
•	Stored BMI value using session state to reuse for analytics.
________________________________________
4. Analytics Visualization
•	Added Analytics Button.
•	Used Matplotlib bar chart to show BMI ranges.
•	Displayed a horizontal line indicating the user’s BMI.
________________________________________
5. UI Enhancements
•	Google Fonts integration.
•	Transparent containers.
•	Gradient BMI result card.
•	Sidebar navigation.
•	“Get Started” landing page with a light background.
________________________________________
6. Deployment
•	Prepared requirements.txt.
•	Uploaded project to GitHub repository.
•	Ready for deployment on platforms like:
o	Streamlit Cloud
o	Render
o	Hugging Face Spaces


Project Hugging Face Link
https://huggingface.co/spaces/ArumugaSelvi/FitPlan-AI-Milestone1

Technologies Used:
Python

Streamlit

HTML

CSS

Matplotlib

GitHub

Deployment Platforms (Hugging Face Spaces)




