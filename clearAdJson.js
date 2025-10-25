// clearAdJson.js
// 将返回体中包含 "ad" / "splash" / "open_screen" 字段的 JSON 清除这些字段，保留其它业务数据。
// 上传到 GitHub 后在 Surge 的 [Script] 区块中引用（type=http-response）。
try {
  var body = $response.body || "";
  if (!body) { $done({}); }
  var obj = JSON.parse(body);
  function removeAds(o) {
    if (!o || typeof o !== 'object') return o;
    for (var k in o) {
      if (!Object.prototype.hasOwnProperty.call(o, k)) continue;
      try {
        var lk = k.toLowerCase();
        if (lk.indexOf('ad') !== -1 || lk.indexOf('splash') !== -1 || lk.indexOf('launch') !== -1 || lk.indexOf('open_screen') !== -1) {
          delete o[k];
        } else {
          removeAds(o[k]);
        }
      } catch (e) {}
    }
  }
  removeAds(obj);
  $done({body: JSON.stringify(obj)});
} catch (e) {
  // 如果解析失败，则不过滤，避免破坏响应
  $done({});
}
