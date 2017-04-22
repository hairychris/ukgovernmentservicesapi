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
ENV CHROMEDRIVER_VERSION 2.28
ENV CHROMEDRIVER_SHA256 8f5b0ab727c326a2f7887f08e4f577cb4452a9e5783d1938728946a8557a37bc
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
  && echo "$CHROMEDRIVER_SHA256  chromedriver_linux64.zip" | sha256sum -c - \
  && unzip "chromedriver_linux64.zip" -d /usr/local/bin \
  && rm "chromedriver_linux64.zip"

# Expose port 8000 for uwsgi
EXPOSE 8001

# Start the USWSGI app
ENTRYPOINT ["uwsgi", "--ini", "./uwsgi.ini"]