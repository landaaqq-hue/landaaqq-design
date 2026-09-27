from flask import Flask, render_template_string
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-123'
socketio = SocketIO(app, cors_allowed_origins="*")

chat_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق المراسلة الآمن</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #0b0f19; color: #f8fafc; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        
        /* شاشة تسجيل الاسم */
        #login-screen { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background: #0b0f19; }
        #login-screen h2 { color: #38bdf8; margin-bottom: 20px; }
        #login-screen input, #login-screen button { padding: 12px; font-size: 16px; border-radius: 8px; border: none; outline: none; margin: 5px; width: 250px; }
        #login-screen input { background: #1e293b; color: #fff; border: 1px solid #334155; text-align: center; }
        #login-screen button { background: #0ea5e9; color: #fff; font-weight: bold; cursor: pointer; transition: 0.2s; }
        #login-screen button:hover { background: #0284c7; }

        /* واجهة الشات الرئيسية */
        #chat-screen { display: none; flex-direction: column; height: 100vh; max-width: 500px; margin: 0 auto; width: 100%; background: #0f172a; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        
        /* الهيدر (صورة واسم التطبيق) */
        .app-header { background: #1e293b; padding: 15px; display: flex; align-items: center; border-bottom: 1px solid #334155; }
        .app-logo { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; border: 2px solid #38bdf8; margin-left: 12px; background: #0ea5e9; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px; color: white; }
        .app-title h3 { margin: 0; font-size: 18px; color: #f8fafc; }
        .app-title span { font-size: 12px; color: #10b981; display: flex; align-items: center; gap: 4px; }
        .app-title span::before { content: ''; width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; }

        /* صندوق الرسائل */
        #box { flex: 1; overflow-y: scroll; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        
        /* تصميم فقاعات الرسائل */
        .msg-container { display: flex; flex-direction: column; max-width: 75%; }
        .msg-container.my-msg { align-self: flex-start; }
        .msg-container.other-msg { align-self: flex-end; }
        
        .sender-name { font-size: 11px; color: #94a3b8; margin-bottom: 3px; padding: 0 4px; }
        .msg-bubble { padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.4; word-break: break-word; }
        
        .my-msg .msg-bubble { background: #0284c7; color: #fff; border-bottom-right-radius: 2px; }
        .other-msg .msg-bubble { background: #334155; color: #f1f5f9; border-bottom-left-radius: 2px; }

        /* شريط الإرسال السفلي */
        .chat-footer { padding: 12px; background: #1e293b; display: flex; gap: 8px; border-top: 1px solid #334155; }
        .chat-footer input { flex: 1; padding: 10px 14px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 8px; outline: none; font-size: 14px; }
        .chat-footer button { padding: 0 20px; background: #10b981; color: #fff; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .chat-footer button:hover { background: #059669; }
    </style>
</head>
<body>

    <!-- شاشة إدخال الاسم -->
    <div id="login-screen">
        <h2>🔐 انضمام إلى الشات الآمن</h2>
        <input type="text" id="username" placeholder="اكتب اسمك المستعار..." autocomplete="off">
        <button onclick="startChat()">دخول المحادثة</button>
    </div>

    <!-- واجهة التطبيق الرئيسية -->
    <div id="chat-screen">
        <div class="app-header">
            <!-- صورة رمزية أو لوجو التطبيق -->
            <div class="app-logo">💬</div>
            <div class="app-title">
                <h3>تطبيق المراسلة الآمن</h3>
                <span>متصل الآن</span>
            </div>
        </div>
        
        <div id="box"></div>
        
        <div class="chat-footer">
            <input id="m" placeholder="اكتب رسالتك هنا..." autocomplete="off" onkeypress="checkEnter(event)">
            <button onclick="sendMsg()">إرسال</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        var socket = io();
        var myName = "";

        function startChat() {
            var inputName = document.getElementById('username').value.trim();
            if(inputName !== "") {
                myName = inputName;
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('chat-screen').style.display = 'flex';
            } else {
                alert("يرجى كتابة الاسم أولاً!");
            }
        }

        socket.on('message', function(data) {
            var box = document.getElementById('box');
            var isMe = (data.name === myName);
            var msgClass = isMe ? 'my-msg' : 'other-msg';
            
            var html = '<div class="msg-container ' + msgClass + '">' +
                       '<span class="sender-name">' + data.name + '</span>' +
                       '<div class="msg-bubble">' + data.msg + '</div>' +
                       '</div>';
            
            box.innerHTML += html;
            box.scrollTop = box.scrollHeight;
        });

        function sendMsg() {
            var input = document.getElementById('m');
            if(input.value.trim() !== '') {
                socket.send({name: myName, msg: input.value});
                input.value = '';
            }
        }

        function checkEnter(e) {
            if(e.key === 'Enter') {
                sendMsg();
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(chat_html)

@socketio.on('message')
def handle(data):
    send(data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
