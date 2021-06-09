import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filter',
  pure: false
})
export class FilterPipe implements PipeTransform {
  transform(items: any[], searchText: string, searchField: string): any[] {
    if (!searchText) return items;
    if (!items) {
      return [];
    } else {
      return items.filter(it => {
        return it[searchField].toLowerCase().includes(searchText.toLowerCase());
      });
  }
}
}
