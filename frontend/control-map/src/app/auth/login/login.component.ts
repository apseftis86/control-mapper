import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {MatTabChangeEvent} from '@angular/material/tabs';
import {AuthService} from '../_services/auth.service';
import {Router} from '@angular/router';
import {AlertService} from '../../alert/alert.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  registerForm: FormGroup;
  user = {} as any;
  registerUser = {} as any;
  action = 'login';
  showPassword = false;
  error = {
    username: null,
    first_name: null,
    last_name: null,
    email:  null,
    password1: null,
    password2:  null,
  };
  constructor(private authService: AuthService, private router: Router,
              private fb: FormBuilder,
              private alertService: AlertService) {}

  ngOnInit() {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required]],
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password1: ['', [Validators.required, Validators.minLength(6)]],
      password2: ['', Validators.required]
    }, {
      validator: this.MustMatch('password1', 'password2')
    });
  }
  get f() { return this.registerForm.controls; }
  MustMatch(controlName: string, matchingControlName: string) {
    return (formGroup: FormGroup) => {
      const control = formGroup.controls[controlName];
      const matchingControl = formGroup.controls[matchingControlName];
      if (matchingControl.errors && !matchingControl.errors.mustMatch) {
        // return if another validator has already found an error on the matchingControl
        return;
      }
      // set error on matchingControl if validation fails
      if (control.value !== matchingControl.value) {
        matchingControl.setErrors({mustMatch: true});
      }
    };
  }
  getKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      if (this.action === 'login' ) {
        this.login();
      }
    }
  }
  login() {
    this.authService.login(this.user.username, this.user.password)
      .subscribe(
          data => {
            this.router.navigate(['/dashboard']);
          },
          err => {
            let error;
            if (err) {
              error = err;
            } else {
              error = 'You could not be logged in.';
            }
            this.alertService.alert('error', error);
          });
  }
  toggleShowPassword() {
    this.showPassword = ! this.showPassword;
  }
  handleTabChange(event: MatTabChangeEvent) {
    if (event.index === 0) {
      this.action = 'login';
      this.user = {} as any;
    } else {
      this.action = 'register';
      this.registerUser = {} as any;
    }
  }
  register() {
    this.authService.register(this.registerForm.value).subscribe((response) => {
      this.alertService.alert('info', response);
    });
  }
}
