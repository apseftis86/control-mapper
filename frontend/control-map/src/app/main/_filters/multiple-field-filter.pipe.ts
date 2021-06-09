import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'multiFieldFilter',
  pure: false
})
export class MultipleFieldFilterPipe implements PipeTransform {
  transform(items: any[], searchText: string, filterFields: any): any[] {
    if (!searchText) return items;
    if (!items) {
      return [];
    } else {
      return items.filter(it => {
        return Array.from(filterFields).some((attr: any) => {
          return it[attr].toLowerCase().includes(searchText.toLowerCase());
        });
      });
    }
  }
}
