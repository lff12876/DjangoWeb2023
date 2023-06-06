(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-90b92106"],{9406:function(e,s,t){"use strict";t.r(s);var i=function(){var e=this,s=e.$createElement,t=e._self._c||s;return t("div",{staticClass:"dashboard-container"},[t("el-card",{staticClass:"box-card"},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("用户信息")])]),t("el-descriptions",{staticClass:"margin-top",attrs:{title:"基本信息",column:2,size:e.size,border:""}},[t("template",{slot:"extra"},[t("el-button",{attrs:{type:"primary",size:"small"},on:{click:function(s){e.dialogFormVisible=!0}}},[e._v("修改密码")])],1),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-user"}),e._v(" 用户名 ")]),e._v(" "+e._s(e.username)+" ")],2),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-postcard"}),e._v(" 用户类别 ")]),t("el-tag",{attrs:{size:"small"}},[e._v(e._s(e.roles[0]))])],2),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-message"}),e._v(" 用户邮箱 ")]),e._v(" "+e._s(e.email)+" ")],2),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-time"}),e._v(" 上次登录 ")]),e._v(" "+e._s(e.last_login)+" ")],2)],2)],1),t("el-divider",[t("i",{staticClass:"el-icon-paperclip"})]),t("el-card",{staticClass:"box-card"},[t("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[t("span",[e._v("业务信息")]),t("el-button",{staticStyle:{float:"right",padding:"3px 0"},attrs:{type:"text"},on:{click:e.external_link}},[e._v("前往购买")])],1),t("el-descriptions",{staticClass:"margin-top",attrs:{title:"当日数据查询",column:2,size:e.size,border:""}},[t("template",{slot:"extra"},[t("el-button",{attrs:{type:"primary",size:"small"},on:{click:e.business_info_1}},[t("i",{staticClass:"el-icon-search"}),e._v("详情")])],1),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-user"}),e._v(" 剩余次数 ")]),e._v(" "+e._s(e.times)+"次 ")],2),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-user"}),e._v(" 业务状态 ")]),t("el-tag",{attrs:{size:"small",type:"success"}},[e._v("正常")])],2)],2),t("el-divider",[t("i",{staticClass:"el-icon-paperclip"})]),t("el-descriptions",{staticClass:"margin-top",attrs:{title:"复盘数据查询",column:2,size:e.size,border:""}},[t("template",{slot:"extra"},[t("el-button",{attrs:{type:"primary",size:"small"},on:{click:e.business_info_2}},[t("i",{staticClass:"el-icon-search"}),e._v("详情")])],1),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-user"}),e._v(" 截至时间 ")]),e._v(" "+e._s(e.fin_time)+" ")],2),t("el-descriptions-item",[t("template",{slot:"label"},[t("i",{staticClass:"el-icon-user"}),e._v(" 业务状态 ")]),t("el-tag",{attrs:{size:"small",type:"success"}},[e._v(e._s(e.business_activate[0]))])],2)],2)],1),t("el-dialog",{attrs:{title:"修改密码",visible:e.dialogFormVisible,center:""},on:{"update:visible":function(s){e.dialogFormVisible=s}}},[t("div",{staticClass:"login-container"},[t("el-form",{ref:"loginForm",staticClass:"login-form",attrs:{model:e.loginForm,rules:e.loginRules}},[t("div",{staticClass:"title-container"},[t("h3",{staticClass:"title"},[e._v("修改密码")])]),t("el-tooltip",{attrs:{content:"大写锁已打开",placement:"right",manual:""},model:{value:e.capsTooltip,callback:function(s){e.capsTooltip=s},expression:"capsTooltip"}},[t("el-form-item",{attrs:{prop:"password"}},[t("span",{staticClass:"svg-container"},[t("svg-icon",{attrs:{"icon-class":"password"}})],1),t("el-input",{key:e.passwordType,ref:"password",attrs:{type:e.passwordType,placeholder:"新密码",tabindex:"2",autocomplete:"on"},on:{blur:function(s){e.capsTooltip=!1}},nativeOn:{keyup:[function(s){return e.checkCapslock(s)},function(s){return!s.type.indexOf("key")&&e._k(s.keyCode,"enter",13,s.key,"Enter")?null:e.handleLogin(s)}]},model:{value:e.loginForm.password,callback:function(s){e.$set(e.loginForm,"password",s)},expression:"loginForm.password"}}),t("span",{staticClass:"show-pwd",on:{click:e.showPwd}},[t("svg-icon",{attrs:{"icon-class":"password"===e.passwordType?"eye":"eye-open"}})],1)],1)],1),t("el-tooltip",{attrs:{content:"大写锁已打开",placement:"right",manual:""},model:{value:e.recapsTooltip,callback:function(s){e.recapsTooltip=s},expression:"recapsTooltip"}},[t("el-form-item",{attrs:{prop:"repassword"}},[t("span",{staticClass:"svg-container"},[t("svg-icon",{attrs:{"icon-class":"password"}})],1),t("el-input",{key:e.repasswordType,ref:"repassword",attrs:{type:e.repasswordType,placeholder:"确认密码",tabindex:"3",autocomplete:"on"},on:{blur:function(s){e.recapsTooltip=!1}},nativeOn:{keyup:function(s){return e.recheckCapslock(s)}},model:{value:e.loginForm.repassword,callback:function(s){e.$set(e.loginForm,"repassword",s)},expression:"loginForm.repassword"}}),t("span",{staticClass:"show-pwd",on:{click:e.reshowPwd}},[t("svg-icon",{attrs:{"icon-class":"password"===e.repasswordType?"eye":"eye-open"}})],1)],1)],1)],1)],1),t("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[t("el-button",{on:{click:function(s){e.dialogFormVisible=!1}}},[e._v("取 消")]),t("el-button",{attrs:{type:"primary"},on:{click:function(s){e.handleChangePWd(),e.dialogFormVisible=!1}}},[e._v("确 定")])],1)])],1)},a=[],o=t("1da1"),r=t("5530"),l=(t("96cf"),t("5880")),n=t("c24f"),c={name:"Dashboard",computed:Object(r["a"])({},Object(l["mapGetters"])(["username","roles","email","business_activate","times","fin_time","last_login","id"])),data:function(){var e=this,s=function(e,s,t){s.length<6?t(new Error("密码不能少于6位")):t()},t=function(s,t,i){""===t?i(new Error("请再次输入密码")):t!==e.loginForm.password?i(new Error("两次输入密码不一致!")):i()};return{size:"",dialogFormVisible:!1,formLabelWidth:"120px",loginForm:{password:"",repassword:""},loginRules:{password:[{required:!0,trigger:"blur",validator:s}],repassword:[{required:!0,trigger:"blur",validator:t}]},capsTooltip:!1,passwordType:"password",recapsTooltip:!1,repasswordType:"password",redirect:void 0}},watch:{$route:{handler:function(e){this.redirect=e.query&&e.query.redirect},immediate:!0}},methods:{showPwd:function(){var e=this;"password"===this.passwordType?this.passwordType="":this.passwordType="password",this.$nextTick((function(){e.$refs.password.focus()}))},checkCapslock:function(e){var s=e.key;this.capsTooltip=s&&1===s.length&&s>="A"&&s<="Z"},reshowPwd:function(){var e=this;"password"===this.repasswordType?this.repasswordType="":this.repasswordType="password",this.$nextTick((function(){e.$refs.repassword.focus()}))},recheckCapslock:function(e){var s=e.key;this.recapsTooltip=s&&1===s.length&&s>="A"&&s<="Z"},jumpUrl:function(e){var s=window.location.protocol+"//"+e;window.open(s,"_blank")},business_info_1:function(){this.$alert("当日数据查询业务，仅能查询当日数据。","业务说明",{confirmButtonText:"确定"})},business_info_2:function(){this.$alert("复盘数据查询业务，业务激活后，在业务到期前，用户可自由查询当日数据和历史数据数据。","业务说明",{confirmButtonText:"确定"})},external_link:function(){this.jumpUrl("www.taobao.com")},handleChangePWd:function(){var e=this,s=this.$store.state.user.id;this.$refs.loginForm.validate((function(t){if(!t)return console.log("error submit!!"),!1;e.loading=!0,Object(n["a"])(e.loginForm,s).then(function(){var s=Object(o["a"])(regeneratorRuntime.mark((function s(t){return regeneratorRuntime.wrap((function(s){while(1)switch(s.prev=s.next){case 0:if(202!==t.status){s.next=9;break}return e.$message({message:"修改成功，请重新登录。",type:"success"}),s.next=4,e.$store.dispatch("user/logout");case 4:e.$router.push("/login?redirect=".concat(e.$route.fullPath)),e.$router.push({path:e.redirect||"/"}),e.loading=!1,s.next=10;break;case 9:e.$message({message:"修改失败",type:"error"});case 10:case"end":return s.stop()}}),s)})));return function(e){return s.apply(this,arguments)}}())}))}}},p=c,d=(t("aeac"),t("2877")),u=Object(d["a"])(p,i,a,!1,null,"4108fb4a",null);s["default"]=u.exports},"99e8":function(e,s,t){},aeac:function(e,s,t){"use strict";t("99e8")}}]);