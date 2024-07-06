# Use the official Node.js 14 image
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Initialize a new Node.js project without prompts
RUN npm init -y

# Install dependencies
RUN npm install express
RUN npm install mongodb
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["node", "index.js"]

