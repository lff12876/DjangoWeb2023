(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-28cb49d2"],{"4e70":function(t,e,s){"use strict";s.d(e,"b",(function(){return c})),s.d(e,"a",(function(){return r})),s.d(e,"c",(function(){return n}));var a=s("b775");function c(t){return Object(a["a"])({url:"/secretkey/",method:"post",params:t})}function r(t,e){return Object(a["a"])({url:"/secretkey/"+e+"/",method:"patch",params:t})}function n(t){return Object(a["a"])({url:"/link/",method:"get",params:t})}},a842:function(t,e,s){},ce56:function(t,e,s){"use strict";s("a842")},d569:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"app-container"},[s("el-card",{staticClass:"box-card"},[s("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[s("span",[t._v("说明")])]),s("div",{staticClass:"text item"},[t._v(" 注：点击右侧按钮申请密钥。 ")]),s("div",{staticClass:"text item"},[t._v(" -- 用户最多拥有一个密钥。 ")]),s("div",{staticClass:"text item"},[t._v(" -- 两种业务密钥互通。 ")]),s("div",{staticClass:"text item"},[t._v(" -- 如果您的密钥因公网ip变动被锁定，请前往密钥管理页面重新激活密钥，无需重复申请。 ")]),s("div",{staticClass:"text item"},[t._v(" -- 如果您的密钥因违规操作被禁用，无法再次申请密钥，请联系客服。 ")]),s("el-card",{staticClass:"box-card"},[s("el-button",{staticStyle:{float:"center"},attrs:{type:"primary"},nativeOn:{click:function(e){return e.preventDefault(),t.getSecretKey(e)}}},[t._v("申请密钥")])],1)],1)],1)},c=[],r=s("4e70"),n={data:function(){return{form:{}}},methods:{getSecretKey:function(){var t=this;Object(r["b"])().then((function(e){console.log(e),201===e.status?(t.$message({message:"申请成功，请前往密钥管理页面查看",type:"success"}),t.$router.push({path:t.redirect||"/"}),t.loading=!1):t.$message({message:"密钥申请失败",type:"error"})}))}}},i=n,u=(s("ce56"),s("2877")),o=Object(u["a"])(i,a,c,!1,null,"29890d6e",null);e["default"]=o.exports}}]);