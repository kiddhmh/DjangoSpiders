/**
 * Created by huminghao on 2018/4/23.
 */


function upfile() {
     // 准备formmate，准备文件
     var fd = new FormData();
     fd.append(file.name, file);
     // 创建xhr对象
     var xhr = new XMLHttpRequest();
     //监听状态，实时响应
     // 传输开始事件  send后就执行
     xhr.onloadstart = function (event) {
          console.log('load start');
     }
     //取消上传
     $("#cancel").one('click', function () {
          xhr.abort();
     })
     // ajax过程传输成功|完成事件
     xhr.onload = function (event) {
          console.log('load success');
          var ret = xhr.responseText; // 服务器返回
          console.log(ret);
          document.getElementById('precent').innerHTML = xhr.responseText;
     };
     // ajax 过程发生错误事件
     xhr.onerror = function (event) {
          console.log('传输错误');
     }
     // ajax 取消操作事件
     xhr.onabort = function (event) {
          console.log('操作取消');
     }
     // 不管上传失败或成功|，都会触发
     xhr.onloadend = function (event) {
          console.log('load end');
     }
     //发送请求
     xhr.open('post', 'Handler.ashx', true);  // true表示异步
          xhr.send(fd);
     }

