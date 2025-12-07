#######This section makes sure the other 
# stages are using the same base image and common configuration

######


# makes a lightweight Python image to serve static files
FROM python:3.11-slim
# Set the working directory to be inside  of the container
WORKDIR /app 






# Copy the frontend files into the image
COPY frontend/ ./



# Cloud Run will tell us what port to listen on via $PORT
ENV PORT=8080

# container listens on this port
EXPOSE 8080

# Start a simple HTTP server that serves the current directory
CMD ["sh", "-c", "python -m http.server ${PORT:-8080}"]
