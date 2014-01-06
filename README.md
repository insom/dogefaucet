Dogefaucet
==========

Super-quick Flask Dogecoin Faucet. Mainly an example application for
[Flask-Coin][fc]

[fc]: https://github.com/insom/flask-coin


Quick Start
-----------

    $ pip install -r requirements.txt
    $ cp example.conf your.conf

Then edit your.conf to your liking- wallet passphrase and Recaptcha are
optional, but recommended. If you're using Recaptcha, you'll need
to [register for your own keys][re]

[re]: http://www.google.com/recaptcha/whyrecaptcha

Create the initial database

    $ python main.py your.conf init

For running on http://localhost:5000/

    $ python main.py your.conf



License
-------

Copyright (c) 2014, Aaron Brady

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
