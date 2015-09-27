

var UserModelr = Backbone.Model.extend({

})

var BaseView = Backbone.View.extend({
		close : function(){
			if(this.childViews){
				this.childViews.close();
			}
			this.remove();
		}
	});

var BaseRouter = Backbone.Router.extend({
	before: function(){},
	after: function(){},
	route : function(route, name, callback){
		if (!_.isRegExp(route)) route = this._routeToRegExp(route);
		if (_.isFunction(name)) {
			callback = name;
			name = '';
	 	}
	  	if (!callback) callback = this[name];

	  	var router = this;

	  	Backbone.history.route(route, function(fragment) {
	   		var args = router._extractParameters(route, fragment);
	   		var next = function(){
		    	callback && callback.apply(router, args);
			    router.trigger.apply(router, ['route:' + name].concat(args));
			    router.trigger('route', name, args);
			    Backbone.history.trigger('route', router, name, args);
			    router.after.apply(router, args);		
	   		}
	   		router.before.apply(router, [args, next]);
	  	});
		return this;
	}
});


var SessionModel = Backbone.Model.extend({
		
		url : '/rest-auth/session/',

		initialize : function(){
			
			//Check for sessionStorage support
			if(Storage && sessionStorage){
				this.supportStorage = true;
			}
		},

		get : function(key){
			if(this.supportStorage){
				var data = sessionStorage.getItem(key);
				if(data && data[0] === '{'){
					return JSON.parse(data);
				}else{
					return data;
				}
			}else{
				return Backbone.Model.prototype.get.call(this, key);
			}
		},


		set : function(key, value){
			if(this.supportStorage){
				sessionStorage.setItem(key, value);
			}else{
				Backbone.Model.prototype.set.call(this, key, value);
			}
			return this;
		},

		unset : function(key){
			if(this.supportStorage){
				sessionStorage.removeItem(key);
			}else{
				Backbone.Model.prototype.unset.call(this, key);
			}
			return this;	
		},

		clear : function(){
			if(this.supportStorage){
				sessionStorage.clear();  
			}else{
				Backbone.Model.prototype.clear(this);
			}
		},

		emp_register:function(credentials){
			console.log("in SessionModel:register()")
			var that = this;
			var register = $.ajax({
				url:'/rest-auth/registration/employee/',
				data : credentials,
				type : 'POST'
			})

			register.done(function(response){
				console.log("in SessionModel:register().done")
				var successMessage = new NotificationView({
				    type: 'success',
				    text: 'New shop created !!!',
				    
				});
				

				console.log("registration response:",response)
				console.log("old csrf:", $('meta[name="csrf-token"]').attr('content') )
				console.log("new csrf:",response.csrf_token)
				$('meta[name="csrf-token"]').attr('content',response.csrf_token)
				console.log("setting session.authenticated to false")
				// that.set('authenticated', false);
				// that.set('user', '');
				dashboardView.myShops();

			})

			register.fail(function(response){
				
				console.log("in SessionModel:register() - fail")
				that.unset('redirectFrom');
				var errors = JSON.parse(response.responseText)
				var keys = [];
				for (var key in errors) {
				  if (errors.hasOwnProperty(key)) {
				    keys.push(key);
				  }
				}
				var successMessage = new NotificationView({
				    type: 'success',
				    text: errors[keys[0]][0]
				    
				});
				console.log('response - ',errors[keys[0]][0])
			})
		},

		register:function(credentials){
			console.log("in SessionModel:register()")
			var that = this;
			var register = $.ajax({
				url:'/rest-auth/registration/',
				data : credentials,
				type : 'POST'
			})

			register.done(function(response){
				console.log("in SessionModel:register().done")
				var successMessage = new NotificationView({
				    type: 'success',
				    text: 'Successfully Registered. Please verify your mail id',
				    
				});
				

				console.log("registration response:",response)
				console.log("old csrf:", $('meta[name="csrf-token"]').attr('content') )
				console.log("new csrf:",response.csrf_token)
				$('meta[name="csrf-token"]').attr('content',response.csrf_token)
				console.log("setting session.authenticated to false")
				that.set('authenticated', false);
				// that.set('user', '');
				if(that.get('redirectFrom')){
					console.log("redirectFrom:",that.get('redirectFrom'))
					var path = that.get('redirectFrom');
					that.unset('redirectFrom');
					Backbone.history.navigate(path, { trigger : true });
				}else{
					
					Backbone.history.navigate('', { trigger : true });
				}

			})

			register.fail(function(response){
				
				console.log("in SessionModel:register() - fail")
				that.unset('redirectFrom');
				var errors = JSON.parse(response.responseText)
				var keys = [];
				for (var key in errors) {
				  if (errors.hasOwnProperty(key)) {
				    keys.push(key);
				  }
				}
				var successMessage = new NotificationView({
				    type: 'success',
				    text: errors[keys[0]][0]
				    
				});
				console.log('response - ',errors[keys[0]][0])
			})
		},

		forgotpwd:function(toemail){
			pwdReset = $.ajax({
				url:'/rest-auth/password/reset/',
				data:toemail,
				type:'POST',

			})

			pwdReset.done(function(){
				console.log("in SessionModel - forgotpwd() - done")
				router.navigate("resetlinksend",{trigger:true})
			})
			pwdReset.fail(function(){
				console.log("in SessionModel - forgotpwd() - fail")

			})
		},

		change2newpwd:function(newpwd){
			changepwd = $.ajax({
				url:'/rest-auth/password/reset/confirm/',
				data:newpwd,
				type:'POST'
			})

			changepwd.done(function(response){
				console.log("in SessionModel - change2newpwd() - done")
				var successMessage = new NotificationView({
				    type: 'success',
				    text: 'Success.Login with your new password',
				    
				});
				router.navigate('login',{trigger:true})
			})

			changepwd.fail(function(response){
				console.log("in SessionModel - change2newpwd() - fail")
			})
		},

		login : function(credentials){
			console.log("in SessionModel:login()")
			var that = this;
			var login = $.ajax({
				url : '/rest-auth/login/',
				data : credentials,
				type : 'POST'
			});
			login.done(function(response){

				var successMessage = new NotificationView({
				    type: 'success',
				    text: 'You have successfully logged in',
				    
				});
				console.log("in SessionModel:login() - done")
				console.log("old csrf:", $('meta[name="csrf-token"]').attr('content') )
				console.log("new csrf:",response.csrf_token)
				$('meta[name="csrf-token"]').attr('content',response.csrf_token)
				console.log("setting session.authnticated to:",response.auth==="true")
				console.log("user role is:",response.role)
				that.set('authenticated',response.auth);
				console.log("session.authnticated=",that.get("authenticated"))
				that.set('user', response.user);
				that.set('user_role',response.role);
				if(that.get('redirectFrom')){
					console.log('session.redirectFrom:',that.get('redirectFrom'))
					var path = that.get('redirectFrom');
					that.unset('redirectFrom');
					console.log('session.redirectFrom:',that.get('redirectFrom'))
					Backbone.history.navigate(path, { trigger : true });
				}else{
					console.log("response.role:",response.role,JSON.stringify(response.role))
					if (response.role == "owner"){
						Backbone.history.navigate('dashboard', { trigger : true });
					}
					else if (response.role == "employee"){
						that.set('shop_name',response.shopname);
						Backbone.history.navigate('mydocs', { trigger : true });

					}
					// Backbone.history.navigate('home', { trigger : true });
				}
			});
			login.fail(function(response){
				console.log("in SessionModel:login() - fail")
				console.log('response - ',response)
				Backbone.history.navigate('login', { trigger : true });
				
			});
		},

		logout : function(callback){
			var that = this;
			$.ajax({
				url : '/rest-auth/logout/',
				type : 'POST'
			}).done(function(response){
				console.log("in SessionModel:logout()")
				console.log("response")
				//Clear all session data
				that.clear();
				//Set the new csrf token to csrf vaiable and
				//call initialize to update the $.ajaxSetup 
				// with new csrf
				csrf = response.csrf;
				that.initialize();
				callback();
			});
		},

		getAuth : function(callback){
			var that = this;
			var Session = this.fetch();

			Session.done(function(response){
				console.log("sessionfetch - done")
				console.log("setting sessions.authenticated to :",response.auth)
				console.log("user is:",response.user)
				that.set('authenticated', response.auth);
				that.set('user',response.user);
				that.set('user_role',response.user_role)

			});

			Session.fail(function(response){
				console.log("sessionfetch - fail")
				// response = JSON.parse(response.responseText);
				that.clear();
				csrf = 'dfdfdfdfjhsdkjfhskjdfhk'
				csrf = response.csrf !== csrf ? response.csrf : csrf;
				that.initialize();
				Backbone.history.navigate("login",{trigger:true})
			});

			Session.always(callback);
		}
});

var UserModel = Backbone.Model.extend({

		defaults : {
			'firstName' : null,
			'lastName' : null
		},

		getFullName : function(){
			return this.get('firstName') + ' ' + this.get('lastName');
		},

		urlRoot : '/rest-auth/user/'
});
// ============================================================
var Document = Backbone.Model.extend({
	initialize:function(){
		console.log('in DocumentModel')
	},
	fileAttribute:'doc',
	urlRoot : 'http://127.0.0.1:8000/api/documents/'
})

var DocumentView = BaseView.extend({
	
	template:_.template($('#document_item_template').html()),
	render:function(){
		this.$el.append(this.template(this.model.toJSON()))
		return this;
	}
})

var DocumentList = Backbone.Collection.extend({
	model:Document,
	initialize:function(){
		console.log('in DocumentList')
	},
	url: 'http://127.0.0.1:8000/api/documents/',
	search : function(letters){
		if(letters == "") {
			console.log("letters empty")
			return this};
		
		var pattern = new RegExp(letters,"gi");
		// var collection = this.filter(function(model) {
  //               return _.some(_.values(model.pick("name")), function(value) {
  //               	console.log("value:",value)
  //               	console.log("~value.toLowerCase().indexOf(letters):",~value.toLowerCase().indexOf(letters))
  //                   return ~value.toLowerCase().indexOf(letters);
  //               });
  //           });
		var collection2 = this.filter(function(data) {
			console.log('pattern.test(data.get("name")):',data.get("name"))
		  	return pattern.test(data.get("name"));
		});
		console.log("returning:", collection2)
		 return collection2
	}
	// 
})

var DocumentListView = BaseView.extend({
	initialize:function(){
		this.collection.on('add',this.addOne,this);
		this.collection.on('update',this.addOne,this);
		this.collection.on('change',this.addAll,this);
		this.collection.on('reset',this.addAll,this);
	},
	events:{},
	template:_.template($('#documents_template').html()),
	search:function(letters){
		console.log("in documentListView(): search() for:",letters)
		// this.collection.search(letters)
		this.filtered = this.collection.search(letters)
		this.addFiltered();
	},
	createdocument:function(){
		console.log("in DocumentListView: createDocument",this.collection)
		console.log("collegename:",$('#collegename').val())
		var newDocument = new Document()
		var data = new FormData()
		data.append('doc',$('input[name="pdfUpload"]')[0].files[0])
		data.append('name',$('#doc_name').val());

		newDocument.save(data,{
			data:data,
			processData: false,
			contentType: false
		}).done(function(data){
			console.log("in DocumentListView: createDoument() : done")

		}).fail(function(){
			console.log("in DocumentListView: createDoument() : fail")
		})
		this.collection.add(newDocument)
	},
	addOne:function(model){
		console.log("in DocumentListView: addOne()")
		console.log("model:",model)
		var view = new DocumentView({model:model})
		$('#documentlist').append(view.render().el)
	},
	addAll:function(){
		console.log("in DocumentListView: addAll(),",this.collection.length)
		$('#documentlist').html('')
		// $('tr').not(function(){if ($(this).has('th').length){return true}}).remove();
		this.collection.forEach(this.addOne,this)
		return this
	},
	addFiltered:function(){
		console.log("in DocumentListView: addAll(),",this.collection.length)
		$('#documentlist').html('')
		// $('tr').not(function(){if ($(this).has('th').length){return true}}).remove();
		this.filtered.forEach(this.addOne,this)
		return this
	},
	render:function(){
		this.$el.html(this.template())
		return this
	}
})
// ============================================================
var Shop = Backbone.Model.extend({
	urlRoot:'/api/shops/',
	idAttribute:"shop_id"
})

var ShopView =BaseView.extend({	
	tagName:'tr',
	initialize:function(){},
	events:{
		'click .getshop' : 'getDetails'

	},
	getDetails:function(id){
		var that = this
		console.log("in ShopListView(): getshop() :",this.model,this.model.get("shop_id"))
		this.model.fetch().done(function(data){
			console.log("got shopdetails for:",data.shopName)
			Session.set("shop_name",data.shopName)
		})
		
	},
	template:_.template($('#shop_item_template').html()),
	render:function(){
		this.$el.html(this.template(this.model.toJSON()))
		return this
	}
})

var ShopList = Backbone.Collection.extend({
	model:Shop,
	url : '/api/shops/'
})

var ShopListView = BaseView.extend({
	initialize:function(){
		console.log("in ShopListView()")
		this.collection.on('add',this.addOne,this)
		this.collection.on('reset',this.addAll,this)
	},
	template:_.template($('#shops_template').html()),

	addOne:function(shop){
		var shopView = new ShopView({model:shop})
		$('#shoplist').append(shopView.render().el)
	},
	addAll:function(){
		console.log("in ShopListView: addAll(),",this.collection.length)
		$('tr').not(function(){if ($(this).has('th').length){return true}}).remove();
		this.collection.forEach(this.addOne,this)
		return this
	},
	render:function(){
		this.$el.html(this.template())
		return this
	},
})

// ============================================================
var Order = Backbone.Model.extend({
	urlRoot:'/api/orders/'
	// 
})

var OrderView = BaseView.extend({
	template:_.template($("#order_item_template").html()),
	render:function(){
		this.$el.append(this.template(this.model.toJSON()))
		return this
	}
})

var OrderList = Backbone.Collection.extend({
	model:Order,
	initialize:function(){

		_.bindAll(this,'onFetch','executeLongPolling');
	},
	url:'/api/orders/',
	longPolling : false,
  	intervalMinutes : 20,
	startLongPolling : function(intervalMinutes){
		console.log("in startLongPolling---",this.intervalMinutes)
	    this.longPolling = true;
	    if( intervalMinutes ){
	      this.intervalMinutes = intervalMinutes;
	    }
	    this.executeLongPolling();
	},
	stopLongPolling : function(){
	this.longPolling = false;
	},
	executeLongPolling : function(){
		console.log("in execute polling")
		this.fetch({success : this.onFetch,update:true});
	},
	onFetch : function () {
		console.log("in fetch after polling----",this.longPolling)
		if( this.longPolling ){
		  setTimeout(this.executeLongPolling, 1000  * 10); // in order to update the view each N minutes
		 }
	}
})

var OrderListView = BaseView.extend({
	initialize:function(){
		this.collection.on('add',this.addOne,this);
		this.collection.on('update',this.addOne,this);
		this.collection.on('change',this.addAll,this);
		this.collection.on('reset',this.addAll,this);
	},
	template:_.template($('#home_template').html()),
	events:{
		'click .emp' : 'test'
	},
	test:function(){
		Session.emp_register()
	},
	addOne:function(model){
		var view = new OrderView({model:model})
		$('#orderlist').append(view.render().el)
	},
	addAll:function(){
		console.log("in OrderListView(): addAll() : length",this.collection.length)
		$('#orderlist').html('')
		this.collection.forEach(this.addOne,this)
		return this
	},
	render:function(){
		this.$el.html(this.template());
		return this;
	}
})
// ============================================================
var ShopProfileView = BaseView.extend({
	initialize:function(){},
	events:{},
	template:_.template($('#shop_profile_template').html()),
	render:function(){
		this.$el.html(this.template())
		return this;
	}
})
var Session = new SessionModel()

var orderList = new OrderList()
var orderListView = new OrderListView({collection:orderList})
var documentList = new DocumentList()
var documentListView = new DocumentListView({collection:documentList})
var shopList = new ShopList()
var shopListView = new ShopListView({collection:shopList})

// orderList.startLongPolling();


var Router = BaseRouter.extend({

		routes : {
			'myorders' : 'showMyOrders',
			'dashboard/addshop' : 'showAddShop',
			'dashboard/myshops' : 'showMyShops',
			'dashboard' 	: 'showDashboard',
			'shops' 		: 'showShops',
			'mydocs' 		: 'showmydocs',
			'resetlinksend' : 'showResetLinkSend',
			'forgotpwd' 	: 'showForgotPwd',
			'pwdreset/:uid/:token' : 'showResetForm',
			'verify-email' 	: 'showVerifyEmail',
			'registration' 	: 'showRegistration',
			'login' 		: 'showLogin',
			'profile' 		: 'showProfile',
			'home' 			: 'showHome',
			''				:'showHome'
		},

		// Routes that need authentication and if user is not authenticated
		// gets redirect to login page
		requiresAuth : ['#profile','#home','',"#mydocs"],
		// pages that can be accessed by owners only
		onlyOwners : ['#dashboard','#dashboard/myshops','#dashboard/addshop'],
		// Routes that should not be accessible if user is authenticated
		// for example, login, register, forgetpasword ...
		preventAccessWhenAuth : ['#login','#registration','#pwdreset','#forgotpwd'],

		before : function(params, next){
			//Checking if user is authenticated or not
			//then check the path if the path requires authentication 
			console.log("in router:before()");

			console.log("Session.get('authenticated'):",Session.get('authenticated'))
			console.log("Backbone.history.location.hash:",Backbone.history.location)
			var isAuth = Session.get('authenticated') === "true";
			var path = Backbone.history.location.hash;
			var needAuth = _.contains(this.requiresAuth, path);
			var cancleAccess = _.contains(this.preventAccessWhenAuth, path);

			var needOwners = _.contains(this.onlyOwners, path)
			var isEmployee = Session.get('user_role') === "employee"
			console.log("needAuth:",needAuth)
			console.log("!isAuth:",!isAuth)

			if(needAuth && !isAuth){
				//If user gets redirect to login because wanted to access
				// to a route that requires login, save the path in session
				// to redirect the user back to path after successful login
				Session.set('redirectFrom', path);
				Backbone.history.navigate('login', { trigger : true });
			}else if(isAuth && cancleAccess){
				//User is authenticated and tries to go to login, register ...
				// so redirect the user to home page
				Backbone.history.navigate('home', { trigger : true });
			}else if(needOwners && isEmployee){
				console.log("Permission granted for OWNERS only !!!")
				Backbone.history.navigate('', { trigger : true });

			}else{
				//No problem handle the route
				console.log("in router: before(): going to next:")
				return next();
			}			
		},

		after : function(){
			//empty
			// 
		},

		changeView : function(view){
			//Close is a method in BaseView
			//that check for childViews and 
			//close them before closing the 
			//parentView
			function setView(view){
				if(this.currentView){
					this.currentView.close();
				}
				this.currentView = view;
				$('.main-container').html(view.render().$el);
			}

			setView(view);
		},

		showAddShop:function(){
			console.log("in router(): showDashboard(): ")
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)
			
			this.changeView(dashboardView);
			dashboardView.addShop();
		},

		showMyShops:function(){

			this.showDashboard()
		},

		showDashboard:function(){
			// leftMenuView.remove()
			$('.leftnav').empty()
			$('.rightnav').empty()
			console.log("in router(): showDashboard(): ")
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)
			
			this.changeView(dashboardView);
			dashboardView.myShops();
			dashboardView.delegateEvents();
		},

		showShops:function(){
			
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)
			shopList.fetch({reset:true})
			.done(function(data){
				console.log("No.of fetched shops are:",data.length)
			})
			this.changeView(shopListView);
		},

		showMyOrders:function(){
			
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)
			// $('.document_container').html(documentListView.render())

			this.changeView(employeeMainView);
			Backbone.trigger('showMyOrders_event')
		},

		showmydocs:function(){
			console.log("in router(): showmydocs(): ")		

			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)

			this.changeView(employeeMainView);
			Backbone.trigger('showMyDocs_event')		
		},

		showResetLinkSend:function(){
			console.log("in router(): showResetLinkSend()")
			var resetlinksend = new ResetLinkSendView()
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Register').el)
			this.changeView(resetlinksend)
		},

		showForgotPwd:function(){
			console.log("in router(): showForgotPwd")
			var forgotpwdView = new ForgotPwdView();
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Register').el)
			this.changeView(forgotpwdView)
		},

		showResetForm:function(uid,token){

			console.log("in router(): showresetForm")
			console.log("uid:",uid);
			console.log("token:",token)
			var pwdResetView =new PwdResetView({uid:uid,token:token});
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Register').el)
			this.changeView(pwdResetView)
		},

		showRegistration:function(){
			console.log("in router:showRegistration()")
			var registrationView = new RegistrationView();
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Login').el)
			this.changeView(registrationView)
		},

		showLogin : function(){
			console.log("in router: showLogin()")
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Register').el)
			var loginView = new LoginView();
			this.changeView(loginView);
		},

		showVerifyEmail:function(){
			console.log("in router: showVerifyEmail()")
			var verifyEmailView = new VerifyEmailView();
			this.changeView(verifyEmailView)
		},

		showProfile : function(){
			console.log("in router: showProfile()")
			console.log("Session.get('user').id",Session.get('user').id)
			var that = this;
			var userModel = new UserModel({
				id : Session.get('user').id
			});
			userModel.fetch()
				.done(function(){
					console.log("in router: showProfile() userModel.fetch - done")
					console.log("userModel:" ,userModel)
					var profileView = new ProfileView({
						model : userModel
					});
					var headerView = new HeaderView();
					$('.header').html(headerView.render('Logout').el)
					that.changeView(profileView);
				})
				.fail(function(error){
					console.log("in router: showProfile() userModel.fetch - fail")
					//In case that session expired
					that.fetchError(error);
				});
		},

		showHome : function(){

			orderList.fetch({reset:true}).done(function(data){
				console.log("in router(): showHome(): - done ",data)
			})
			
			var homeView = new HomeView();
			var headerView = new HeaderView();
			
			$('.header').html(headerView.render('Logout').el)
			this.changeView(orderListView);
		},

		fetchError : function(error){
			//If during fetching data from server, session expired
			// and server send 401, call getAuth to get the new CSRF
			// and reset the session settings and then redirect the user
			// to login
			console.log("in fetchError with:",error.status)
			if(error.status === 401){
				console.log("having a 401")
				Session.getAuth(function(){
					Backbone.history.navigate('login', { trigger : true });
				});
			}
		}
});

var AddShopView = BaseView.extend({
	initialize:function(){},
	events:{
		'click .createshop':'createshop'
	},
	createshop:function(){
		var shopname = $('#shopname').val()
		var username = $('#username').val()
		var password1 = $('#password1').val()
		var password2 = $('#password2').val()

		Session.emp_register({
			'shopName':shopname,
			'username' : username,
			'password1' : password1,
			'password2' : password2
		})
	},
	template:_.template($('#addshop_template').html()),
	render:function(){
		this.$el.html(this.template({
			'username' : Session.get('user')
		}))
		return this
	}
})

var LeftMenuView = BaseView.extend({
	initialize:function(){
		this.subModal = '' 
		Backbone.on('shoMyDocs',this.myDocs)
		Backbone.on('myOrders',this.myOrders)

			
	},
	events:{
		'click .shop_profile' : 'shopProfile',
		'click #add_document' : 'createdocument',
		'change .doc_type' : 'typeModal',
		'click #doc_type' : 'typeModal',
		'click #course' : 'courseModal',
		'change .doc_type_choice':'tester',
		'click .orders' : 'myOrders',
		'click .docs' : 'myDocs',
		'hidden.bs.modal .sub-modal' : 'modalAdjust',
	},
	modalAdjust:function(){

		if(this.subModal == ''){

			        $("#mainform").animate({
			        	 right: 0
			        },"slow");
		}
	},
	shopProfile:function(){
		console.log("hereeeeeeeeeeeeeeeeeeeeeeee")
		Backbone.trigger('showShopProfile_event')
		router.navigate('profile')
	},
	myDocs:function(){
		Backbone.trigger('showMyDocs_event')
		router.navigate('mydocs')
	},
	myOrders:function(){
		Backbone.trigger('showMyOrders_event')
		router.navigate('myorders')

	},
	createdocument:function(){
		documentListView.createdocument()
	},
	tester:function(){
		console.log("in tester",$('input[name=options]:checked', '.doc_type_choice').val())
		$("#doc_type").val($('input[name=options]:checked', '.doc_type_choice').val());
		
		if($('input[name=options]:checked', '.doc_type_choice').val()=="Textbook"){
			var textView = new TextView()
			$('.doc_type_form').html(textView.render().el)
		}else{	
			var noteView = new NoteView()
			$('.doc_type_form').html(noteView.render().el)
		}
	},
	courseModal:function(){
		
		console.log("this.subModal:",$("#mainform").css('right'),"::",this.subModal)
		if(this.subModal=="courseModal" || this.subModal=="" ){	
			this.subModal =  this.subModal == "courseModal" ? "":"courseModal"
			$("#mainform").animate({
	        	 right: 190
	        },"slow",function(){
	        	
	        	$('.bs-example3-modal-sm').modal('toggle')
	        });

	       
		}else{
			console.log("already typeModal present",this.subModal)
			$('.type-modal').modal('toggle')
			$('.course-modal').modal('toggle')
			this.subModal =  this.subModal == "courseModal" ? "":"courseModal"
		}
		
		console.log("subModal:::::::",this.subModal)
	},
	typeModal:function(){
		
		if(this.subModal=="typeModal" || this.subModal=="" ){	
			this.subModal = (this.subModal == "typeModal" ? "":"typeModal")
			$("#mainform").animate({
        	 right: 190
        },"slow",function(){
        	$('.bs-example2-modal-sm').modal('toggle')
        });

	       
		}else{
			console.log("already courseModal present",this.subModal)
			$('.course-modal').modal('toggle')
			$('.type-modal').modal('toggle')
			this.subModal = (this.subModal == "typeModal" ? "":"typeModal")
		}
		
		console.log("subModal:::::::",this.subModal)
	 	
	},
	template:_.template($('#leftMenu_template').html()),
	render:function(){
		console.log("in LeftMenuView(): render()")
		this.$el.html(this.template({
			"user_role":Session.get("user_role"),
			"shop_name":Session.get("shop_name")
		}))
		return this
	}
})

var RightMenuView = BaseView.extend({
	initialize:function(){},
	events:{},
	template:_.template($('#rightMenu_template').html()),
	render:function(){
		this.$el.html(this.template())
		return this
	}
})

var DashboardView = BaseView.extend({
	initialize:function(){
		// this.myShops();
	},
	events:{
		'click .myshops' : 'myShops',
		'click .addshop' : 'addShop'
	},
	addShop:function(e){
		// if(e)
		//  { e.preventDefault() }
		var addShopView = new AddShopView()
		$('#dashboard_container').html(addShopView.render().el)
		Backbone.history.navigate('dashboard/addshop')
	},
	myShops:function(e){
		if(e)
		 { e.preventDefault() }
		shopList.fetch({reset:true})
			.done(function(data){
				console.log("No.of fetched shops are:",data.length)
		})
		$('#dashboard_container').html(shopListView.render().el)
		Backbone.history.navigate('dashboard/myshops')
	},
	template:_.template($('#dashboard_template').html()),
	render:function(){
		this.$el.html(this.template())
		return this;
	}
})

var TextView = BaseView.extend({
	template:_.template($('#textbook_template').html()),
	render:function(){
		this.$el.append(this.template())
		return this
	}
})

var NoteView = BaseView.extend({
	template:_.template($('#notebook_template').html()),
	render:function(){
		this.$el.append(this.template())
		return this
	}
})

var RegistrationView = BaseView.extend({
	template: _.template($('#registration_template').html()),
	events:{
		'click #registration' : 'submit'
	},
	render:function(){
		this.$el.html(this.template());
		return this
	},
	submit:function(e){
		e.preventDefault();
		var username = $('#username').val();
		var password1 = $('#password').val();
		var password2 = $('#password').val();
		var email = $('#email').val(); 
		console.log("in submit of registration")
		Session.set('redirectFrom','verify-email')
		Session.register({
			username : username,
			password1:password1,
			password2:password2,
			email:email
		})
	}
})

var ResetLinkSendView = BaseView.extend({
	template:_.template($('#resetlinksend').html()),
	render:function(){
		this.$el.html(this.template())
		return this
	}
})

var ForgotPwdView = BaseView.extend({
	template:_.template($('#forgotpwd').html()),

	events:{
		'click .sendpwd' : 'sendpwd'
	},

	sendpwd:function(){
			console.log("in ForgotPwdView(): sendpwd()")
			tomail = { email:$('#email').val() }
			Session.forgotpwd(tomail);
	},


	render:function(){
		this.$el.html(this.template());
		return this
	}
})

var PwdResetView = BaseView.extend({
	initialize:function(options){
		
    	this.options = options;
    	_.bindAll(this, 'render');
	
	},
	template:_.template($('#pwdreset').html()),
	events:{
		'click .pwdreset' : 'pwdreset'
	},
	pwdreset:function(){
		console.log("in PwdResetView: pwdreset()")
		newpwd = {
			new_password1:$('#password1').val(),
			new_password2:$('#password2').val(),
			uid:this.options.uid,
			token:this.options.token
		}
		Session.change2newpwd(newpwd)	

	},
	render:function(){
		this.$el.html(this.template())
		return this
	}
})

var LoginView = BaseView.extend({

		template : _.template($("#login_template").html()),
		
		events : {
			'click #login' : 'submit',
			'click .forgotpwd' : 'forgotpwd'
		},

		render : function(){
			this.$el.html(this.template());
			console.log("loginview: render(), this:",this)
			return this;
		},

		forgotpwd:function(){
			router.navigate('forgotpwd',{trigger:true})
		},

		submit : function(e){
			console.log("in submit of login")
			e.preventDefault();
			var username = $('#username').val();
			var password = $('#password').val();

			Session.login({
				username : username,
				password : password
			});
		}
});

var VerifyEmailView = BaseView.extend({
	template:_.template($('#verifyemail_template').html()),
	events:{

	},
	render:function(){
		this.$el.html(this.template())
		return this
	}
})

var ProfileView = BaseView.extend({

	template : _.template($("#profile_template").html()),

	events : {
		'click .logout' : 'logout',
		'click .profile_save' : 'save'
	},

	render : function(){
		var url1= "/static/media/documents/"

		// console.log("image:",url1.concat(this.model.toJSON().profile_picture.split('/').pop()))
		if (this.model.toJSON().profile_picture)
			this.$el.html(this.template({'user':this.model.toJSON(),'userimage':url1.concat(this.model.toJSON().profile_picture.split('/').pop())}));
		else
			this.$el.html(this.template({'user':this.model.toJSON(),'userimage':''}));
		return this;
	},
	save :function(){
		console.log("image:",$('input[name="fileInput"]')[0].files[0])
		var data = new FormData();
		if (!$('input[name="fileInput"]')[0].files[0])
			pic = this.model.toJSON().profile_picture
		else
			pic = $('input[name="fileInput"]')[0].files[0]
		data.append('profile_picture',pic)
		data.append('username',$("#username").val())
		data.append('email',$('#email').val())
		data.append('first_name',$('#firstname').val())
		data.append('last_name',$('#lastname').val())
		data.append('company_name',$('#companyname').val())
		userEdit = $.ajax({
			url:'/rest-auth/user/',
			data:data,
			type:'PUT',
			processData: false,
			contentType: false
		})

		userEdit.done(function(response){
			console.log("in ProfileView:",response)
		})
		userEdit.fail({
			
		})
	},
	logout : function(e){
		Session.logout(function(){
			Backbone.history.navigate('login', { trigger : true });
		});
	}
});

var HomeView = BaseView.extend({

	template : _.template($('#home_template').html()),

	events : {
		'click .logout' : 'logOut'
	},

	logOut : function(){
		var view = this;
		Session.logout(function(){
			Backbone.history.navigate('login', { trigger : true });
		});
	},

	render : function(){
		console.log("in HomeView: render()")
		console.log("Session.get('user'):",Session.get('user'))
		var user = Session.get('user');
		this.$el.html(this.template({
			user : user
		}));
		return this;
	}
});

var HeaderView = BaseView.extend({
	template:_.template($('#header_template').html()),
	events : {
		"keyup #searchdoc" : "callSearcher",
		'click .logout'  : 'logout',
		'click .register': 'register',
		'click .login'   : 'login',
		'click .profile' : 'profile',
		'click .shops' : 'shops'  
	},
	callSearcher:function(e){
		var letters = $("#searchdoc").val();
		documentListView.search(letters)

	},
	shops:function(){
		// router.navigate("dashboard",{trigger:true})
	},
	register:function(){
		router.navigate("registration",{trigger:true})
	},
	login:function(){
		router.navigate("login",{trigger:true})
	},
	logout:function(){
		Session.logout(function(){
			Backbone.history.navigate('login', { trigger : true });
		});
	},
	render:function(buttonname){
		var role = Session.get("user_role")
		var username = Session.get("user")

		this.$el.html(this.template({
			'buttonname':buttonname,
			'urll':'trial',
			'username':username,
			'role':role
			}))
		return this
	}
})

var ApplicationModel = Backbone.Model.extend({

	start : function(){
		console.log("in ApplicationModel:start()")
		Session.getAuth(function(response){
			var router = new Router();
			Backbone.history.start();
		});
	}
});

var EmployeeMainView = BaseView.extend({
	initialize:function(){
		console.log("initializing EmployeeMainView()")
		this.leftMenuView = new LeftMenuView()
		this.rightMenuView = new RightMenuView()
		this.shopProfileView = new ShopProfileView()
		
		Backbone.on('showMyDocs_event',this.showMyDocs)
		Backbone.on('showMyOrders_event',this.showMyOrders)
		Backbone.on('showShopProfile_event',this.showShopProfile)

	},
	template:_.template($('#emp_template').html()),
	events:{},
	showShopProfile:function(){
		console.log("in EmployeeMainView(): showShopProfile()")
		new ShopProfileView().setElement(this.$('.centerview')).render();
	},
	showMyDocs:function(){
		console.log("in EmployeeMainView(): showMyDocs()")
		documentList.fetch({reset:true}).done(function(data){
				console.log("in EmployeeMainView(): showMyDocs(): -fetch - done ",data)
				console.log("number of docs:", data.length)
		})
		documentListView.setElement(this.$('.centerview')).render();
	},
	showMyOrders:function(){
		console.log("in EmployeeMainView(): showMyOrders()")
		orderList.fetch({reset:true}).done(function(data){
				console.log("in EmployeeMainView(): showMyOrders(): -fetch - done ",data)
		})
		orderListView.setElement(this.$('.centerview')).render();

	},
	render:function(){
		console.log("in EmployeeMainView(): render();")
		this.$el.html(this.template())
		this.leftMenuView.setElement(this.$('.leftnav')).render();
		this.rightMenuView.setElement(this.$('.rightnav')).render();
		// $('.rightnav').html(this.rightMenuView.render().el)
		return this
	}
})


var app = new ApplicationModel();
app.start(); 
var router = new Router();
var dashboardView = new DashboardView()
var employeeMainView = new EmployeeMainView()

var NotificationView = Backbone.View.extend({
 
    targetElement: '#message',
 
    tagName: 'div',
 
    className: 'notification',        
 
    defaultMessages: {
        'success': 'Success!',
        'error': 'Sorry! An error occurred in the process',
        'warning': 'Are you sure you want to take this action?',
        'information': 'An unknown event occurred'
    }, 
 
    cssClasses: {
        'success': 'accepted',
        'error': 'cancel',
        'warning': 'warning',
        'information': 'information'
    }, 
 
    events: {
        "click" : "closeNotification",
    },
 
    automaticClose: true, 
 
    initialize: function(options){
 
        // defaults
        var type = 'information';
        var text = this.defaultMessages[type]; 
        var target = this.targetElement; 
 
        // if any options were set, override defaults
        if(options && options.hasOwnProperty('type'))
            type = options.type;
        if(options && options.hasOwnProperty('text'))
            text = options.text; 
        if(options && options.hasOwnProperty('target')) 
            target = options.target;
 
        if(options && options.hasOwnProperty('automaticClose'))
        this.automaticClose = options.automaticClose;
 
        // is message already displayed in view? if yes, don't show again
        if($('.notification:contains('+text+')').length === 0) { 
            this.render(type, text, target);
        }
 
    },
 
    render: function(type, text, target){
 		console.log("in NotificationView: render()")
        var self = this;
        this.$el.addClass(this.cssClasses[type]);
        this.$el.text(text);
        this.$el.prependTo(this.targetElement);
 
        // Automatically close after set time. also closes on click
        if(this.automaticClose) {
            setTimeout(function(){
                self.closeNotification();
            }, 3000);
        }
    },
 
    closeNotification: function() {
 
        var self = this;
 
        $(this.el).fadeOut(function() {
            self.unbind(); 
            self.remove(); 
        });
    }
 
});


var vent = _.extend({}, Backbone.Events);

$.ajaxSetup({
    statusCode: {
        401: function(){
            // Redirec the to the login page.
            console.log("got a 401")
            window.location.replace('/#login');
         
        },
        403: function() {
            // 403 -- Access denied
            window.location.replace('/#denied');
        }
    }
});