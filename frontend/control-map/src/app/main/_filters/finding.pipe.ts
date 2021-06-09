import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'findingfilter'
})
export class FindingFilterPipe implements PipeTransform {
  transform(items: any[], searchText: string, searchField: string): any[] {
    if (!items)  return [];
    if (!searchText)  return items;
    return items.filter( it => {
      if (searchField === 'controls') {
        return it[searchField].join(',').toLowerCase().includes(searchText.toLowerCase());
      } else {
        return it[searchField].toLowerCase().includes(searchText.toLowerCase());
      }
    });
  }
}
