var User = Backbone.Model.extend({

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
				that.set('authenticated',response.auth);
				console.log("session.authnticated=",that.get("authenticated"))
				that.set('user', JSON.stringify(response.user));
				if(that.get('redirectFrom')){
					console.log('session.redirectFrom:',that.get('redirectFrom'))
					var path = that.get('redirectFrom');
					that.unset('redirectFrom');
					console.log('session.redirectFrom:',that.get('redirectFrom'))
					Backbone.history.navigate(path, { trigger : true });
				}else{
					Backbone.history.navigate('home', { trigger : true });
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
				that.set('authenticated', response.auth);
				that.set('user', JSON.stringify(response.user));

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

var Session = new SessionModel()

var Router = BaseRouter.extend({

		routes : {
			'resetlinksend' : 'showResetLinkSend',
			'forgotpwd' : 'showForgotPwd',
			'pwdreset/:uid/:token' : 'showResetForm',
			'verify-email' : 'showVerifyEmail',
			'registration' : 'showRegistration',
			'login' : 'showLogin',
			'profile' : 'showProfile',
			'home' : 'showHome',
			'':'showHome'

		},

		// Routes that need authentication and if user is not authenticated
		// gets redirect to login page
		requresAuth : ['#profile','#home',''],

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
			var needAuth = _.contains(this.requresAuth, path);
			var cancleAccess = _.contains(this.preventAccessWhenAuth, path);
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
				$('.container').html(view.render().$el);
			}

			setView(view);
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
			console.log("in router: showHome()")
			var homeView = new HomeView();
			var headerView = new HeaderView();
			$('.header').html(headerView.render('Logout').el)
			this.changeView(homeView);
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
		this.$el.html(this.template(this.model.toJSON()));
		return this;
	},
	save :function(){
		console.log("image:",$('input[name="fileInput"]')[0].files[0])
		var data = new FormData();
		data.append('profile_picture',$('input[name="fileInput"]')[0].files[0])
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
		'click .logout'  : 'logout',
		'click .register': 'register',
		'click .login'   : 'login',
		'click .profile' : 'profile' 
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
		this.$el.html(this.template({'buttonname':buttonname,'urll':'trial','username':''}))
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

var app = new ApplicationModel();
app.start(); 
var router = new Router();


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