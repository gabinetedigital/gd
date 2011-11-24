#!/usr/bin/env node

/* run 'npm install mysql' before executing this */

/* this script creates a question in pairwise for each theme specified
 * below and for each theme, it queries GD's database for all ideas
 * approved and sends them to pairwise as a json text object (containing
 * the gd's DB contrib.id field and its title -- this one, only for
 * checking purposes).
 *
 * Note: the base64 conversion of the title is because pairwise raises
 * exception when the text is not on an acceptable text encoding.
 */


var themes = ['cuidado','familia','emergencia','medicamentos','regional'];

PAIRWISE_URL_PREFIX   = "http://pairuser:pairpass@localhost:4000";

GD_MYSQL_HOST = "localhost";
GD_MYSQL_DB = 'gd_dump'
GD_MYSQL_USER = 'root'
GD_MYSQL_PASS = ''
GD_CONTRIB_TABLE = 'contrib';

///////////////


var D = console.log;
var HTTP = require('http');
var URL = require('url');

function create_question(theme, ideas, count) {
  D(theme + " question with " + count + " ideas");
  var question = {
    question: {
      name: "["+theme+"] Como podemos melhorar o atendimento na saude publica?",
      url: 'musica',
      ideas: ideas,
      information:"",
      'local_identifier':'1',
      'visitor-identifier': 'a4b8c273bfb9a25bf4999c71b0869cb4'
    }};

  var data = JSON.stringify(question);
  var p = URL.parse(PAIRWISE_URL_PREFIX+'/questions.xml');
  var encoded = new Buffer(p.auth).toString('base64');
  var options = {
    port: p.port,
    host: p.hostname,
    path: p.pathname+(p.query?"?"+p.query:''),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + encoded
    }
  };

  options.method = 'POST';
  options.headers['Content-Length'] = data.length

  var req = HTTP.request(options);
  var ret = '';
  req.on('response', function(res) {
    res.on('data', function(d) {
      ret += d });
    res.on('error', function() {
      D("-- error: "+ url);
    });
    res.on('end', function() {
      var id = /<id type="integer">(\d+)<\/id>/.exec(ret)[1];
      console.log("done! question id[" + theme + "]: " +  id);
    });
  });
  req.write(data);
  req.end();
}

function get_gd_choices(theme) {
  var mysql = require('mysql');
  var client = mysql.createClient({
    user: GD_MYSQL_USER,
    password: GD_MYSQL_PASS,
  });

  client.query('USE ' + GD_MYSQL_DB);

  var sql = 'SELECT * FROM '+
    GD_CONTRIB_TABLE +
    " WHERE enabled=1 and status=1 and theme='"+theme+"'";
  client.query(sql, function(err,res) {
    if (err && err.number != mysql.ERROR_DB_CREATE_EXISTS) {
      throw err;
    }
    client.end();

    create_question(theme, res.map(function(x) {
      var title = new Buffer(x.title).toString('base64');

      return '{"id":"'+x.id+'","title":"'+title+'"}';
    }).join("\n"), res.length);
  });
}

themes.forEach(function(theme) {
  get_gd_choices(theme)
});
