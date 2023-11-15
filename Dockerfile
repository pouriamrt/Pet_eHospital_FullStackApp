FROM python:3.11.3
 
# Create app directory
WORKDIR /project
 
# Install app dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .
 
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
