FROM markadams/chromium-xvfb

RUN apt-get update && apt-get install -y \
    python3-minimal python3-pip curl unzip libgconf-2-4

# Create app directory
ADD ./src /webapp
ADD ./requirements.txt /webapp
ADD ./uwsgi.ini /webapp
 
# Set the default directory for our environment
ENV HOME /webapp
WORKDIR /webapp

# Install Python requirements
RUN pip3 install -r requirements.txt

# Install Chromedriver
ENV CHROMEDRIVER_VERSION 2.27
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
  && unzip "chromedriver_linux64.zip" -d /usr/local/bin \
  && rm "chromedriver_linux64.zip"

# Expose port 8000 for uwsgi
EXPOSE 8001

# Start the USWSGI app
ENTRYPOINT ["uwsgi", "--ini", "./uwsgi.ini"]