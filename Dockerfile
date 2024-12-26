FROM python:3.12

WORKDIR /app

COPY . /app

# Install dependencies
RUN pip install -r requirements.txt
RUN pip install openai


# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
