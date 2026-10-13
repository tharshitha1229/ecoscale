# Use official Node runtime as a parent image
FROM node:20-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your backend code
COPY . .

# Expose the port your app runs on (assuming 5001)
EXPOSE 5001

# Command to run your backend
CMD ["node", "server.js"]
