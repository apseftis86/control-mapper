import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HTTP_INTERCEPTORS, HttpClientModule, HttpClientXsrfModule} from '@angular/common/http';
import {JwtInterceptor} from './_interceptors/jwt.interceptor';
import {HttpXSRFInterceptor} from './_interceptors/httpxsrfInterceptor.interceptor';
import {ErrorInterceptor} from './_interceptors/error.interceptor';
import {AppRoutingModule} from '../app-routing.module';
import {HeaderComponent} from './header/header.component';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDialogModule} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {MatInputModule} from '@angular/material/input';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatTabsModule} from '@angular/material/tabs';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatListModule} from '@angular/material/list';
import {MatIconModule} from '@angular/material/icon';
import {HomeService} from './_services/home.service';
import {AuthService} from './_services/auth.service';
import {MatCardModule} from '@angular/material/card';
import {MainModule} from '../main/main.module';
import {MainRoutingModule} from '../main/main-routing.module';
import {ImportModule} from '../import/import.module';
import {ImportRoutingModule} from '../import/import-routing.module';
import { AuthComponent } from './auth.component';



@NgModule({
  declarations: [
    AuthComponent,
    HeaderComponent,
    HomeComponent,
    LoginComponent,
    HeaderComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    AppRoutingModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    MatFormFieldModule,
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatTooltipModule,
    MatTabsModule,
    MatToolbarModule,
    MatListModule,
    MatIconModule,
    MatCardModule,
  ],
  providers: [
    HomeService,
    AuthService,
    // these are only needed if auth module is imported
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true},
    {
      provide: HTTP_INTERCEPTORS, useClass: HttpXSRFInterceptor, multi: true
    },
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
  ],
  exports: [HeaderComponent],
  bootstrap: [AuthComponent]
})
export class AuthModule {}
