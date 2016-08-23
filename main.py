#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, re, cgi

html_head = """
<HTML>
    <head>
        <title>SignUp</title>
    </head>
    <body>
"""

html_end = """
    </body>
</HTML>
"""
form = """
<H2 style="margin: 0 0 0 2px;"> Sign Up </H2>
<span style="font-size: 6; margin-left:4px;"> but for what? </span>
<form action="/welcome" method="post" >
    <table>
        </tbody>
            <tr>
                <td><label for="username"> Username:</label> </td>
                <td><input name="username" type="text"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            
            <tr>
                <td><label for="password"> Password: </label></td>
                <td><input name="password" type="text"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            
            <tr>
                <td><label for="pconfirm"> Confirm Password:</label></td>
                <td><input name="pconfirm" type="text"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            
            <tr>
                <td><label for="email"> Email (optional) </label></td>
                <td><input name="email" type="text"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            <tr>
                <td></td>
                <td style="text-align: right;"><input type="submit"/></td>
            </tr>
        </tbody>
    </table>
</form>

"""
def vali_name(name):
    valid = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return valid.match(name)

def vali_email(email):
    valid = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return valid.match(email)

def vali_pass(pword):
    valid = re.compile(r"^.{3,20}$")
    return valid.match(pword)

class Index(webapp2.RequestHandler):
    ''' handles requests for main index page '''
    def get(self):
        nerror = self.request.get('nerror')
        nerror_element = '<p class="error">' + nerror + "</p>" if nerror else ""
        
        perror = self.request.get('perror')
        perror_element = '<p class="error">' + perror + "</p>" if perror else ""
        
        merror = self.request.get('merror')
        merror_element = '<p class="error">' + merror + "</p>" if merror else ""
        
        eerror = self.request.get('eerror')
        eerror_element = '<p class="error">' + eerror + "</p>" if eerror else ""
        
        self.response.write(html_head + form.format(nerror, perror, merror, eerror) \
                            + html_end)

class Welcome(webapp2.RequestHandler):
    ''' handles requests for welcome success page '''
    def post(self):
        error = ""
        name = self.request.get('username')
        pword = self.request.get('password')
        pconf = self.request.get('pconfirm')
        email = self.request.get('email')
        
        if not vali_name(name):
            error += "nerror=Username Invalid"
            
        if not vali_pass(pword):
            if error != "":
                error += "&"
            error += "perror=Password Invalid"
        
        if not pword == pconf:
            if error != "":
                error += "&"
            error += "merror=Passwords must match"
        
        if email: 
            if not vali_email(email):
                if error != "":
                    error += "&"
                error += "eerror=Email Invalid"
        name = cgi.escape(name)
        pword = cgi.escape(pword)
        pconf = cgi.escape(pconf)
        email = cgi.escape(email)
        
        if error != "":
            self.redirect("/?" + error)
        
        self.response.write(html_head + "Welcome, {}".format(name) + html_end)
        
        
        
        

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
