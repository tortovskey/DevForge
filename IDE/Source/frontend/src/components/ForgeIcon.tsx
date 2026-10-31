export function ForgeIcon({size=24,className=''}:{size?:number;className?:string}){
  return <img src="/forge.svg" alt="" aria-hidden="true" width={size} height={size} className={className} style={{flexShrink:0,display:'inline-block'}}/>;
}
