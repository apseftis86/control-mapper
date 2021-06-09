import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ImportComponent} from './import.component';

const routes: Routes = [
  {path: 'import', component: ImportComponent, data: {isList: true}},
];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ImportRoutingModule { }
